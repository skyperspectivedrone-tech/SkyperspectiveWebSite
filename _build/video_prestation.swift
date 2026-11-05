// Prépare les vidéos web de la page Prestations, en H.264 1280 × 720, démarrage rapide
// (faststart), plus une image d'attente (poster) en JPEG.
//
// Deux usages :
//  - boucle (défaut) : plusieurs extraits enchaînés en coupes franches, SANS son, ~3 Mbit/s.
//    Le poster est la première image, pour que le passage poster → vidéo ne saute pas.
//        swift -suppress-warnings _build/video_prestation.swift <id> <source>:<debut>-<fin> [...]
//    → site/assets/media/prestations/<id>.mp4 et <id>.jpg
//  - film (--film) : une vidéo source entière, AVEC son (AAC 128 kbit/s), ~3,5 Mbit/s.
//        swift -suppress-warnings _build/video_prestation.swift --film [--poster <s>] <id> <source>
//    → site/assets/media/films/<id>.mp4 et <id>.jpg (poster pris à <s> secondes, 25 % par défaut)
//
// Cadence : chaque extrait garde celle de SA source (24, 25, 29,97…) ; au-delà de 30 i/s
// (59,94 des FPV) elle est divisée exactement par deux. Ne jamais forcer une cadence unique :
// 24 i/s rééchantillonné en 30 répète une image sur quatre et la vidéo saccade. Un montage
// qui mêle des sources de cadences différentes donne donc un MP4 à cadence variable,
// ce que tous les navigateurs lisent.
//
// Encodage : pas d'images B (AVVideoAllowFrameReorderingKey à false). Avec elles, l'encodeur
// compressait une image sur deux bien plus fort que ses voisines : la netteté alternait d'une
// image à l'autre (mesuré : 117 / 126 / 117 / 125…) et la vidéo semblait trembler. Le débit a
// été relevé en même temps (boucles 1,8 → 3 Mbit/s) : à 1,8, le grain des routes et des
// feuillages disparaissait en mouvement.
//
// Sans ffmpeg : AVFoundation est livré avec macOS. Chaque extrait est recadré en remplissage
// 16:9 (sources 4K, 1080p ou tournées) et les sources HDR (HLG des DJI) ramenées en SDR Rec. 709.
// Un extrait sans « :debut-fin » est pris en entier.
import AVFoundation
import ImageIO
import UniformTypeIdentifiers

let USAGE = """
  usage : swift -suppress-warnings _build/video_prestation.swift <id> <source>:<debut>-<fin> [...]
          swift -suppress-warnings _build/video_prestation.swift --film [--poster <s>] <id> <source>
  """
var args = Array(CommandLine.arguments.dropFirst())
var modeFilm = false
var tempsPoster: Double? = nil
while let premier = args.first, premier.hasPrefix("--") {
  args.removeFirst()
  switch premier {
  case "--film": modeFilm = true
  case "--poster":
    guard let s = args.first, let v = Double(s) else { print(USAGE); exit(1) }
    tempsPoster = v; args.removeFirst()
  default: print("✗ option inconnue : \(premier)\n\(USAGE)"); exit(1)
  }
}
guard args.count >= 2 else { print(USAGE); exit(1) }
let LARGEUR = 1280, HAUTEUR = 720
let DEBIT = modeFilm ? 3_500_000 : 3_000_000
let rendu = CGSize(width: LARGEUR, height: HAUTEUR)

// "<chemin>:<debut>-<fin>" — découpé sur le dernier « : », le chemin peut contenir des espaces.
struct Extrait { let chemin: String; let debut: Double?; let fin: Double? }
let extraits: [Extrait] = args.dropFirst().map { arg in
  var chemin = arg, debut: Double? = nil, fin: Double? = nil
  if let deuxPoints = arg.lastIndex(of: ":") {
    let temps = arg[arg.index(after: deuxPoints)...].split(separator: "-").compactMap { Double($0) }
    if temps.count == 2 {
      guard temps[1] > temps[0] else { print("✗ temps invalides (debut-fin) : \(arg)"); exit(1) }
      chemin = String(arg[..<deuxPoints]); debut = temps[0]; fin = temps[1]
    }
  }
  guard FileManager.default.fileExists(atPath: chemin) else {
    print("✗ fichier introuvable : \(chemin)")
    print("  Astuce : glisse la vidéo depuis le Finder dans le Terminal pour coller son chemin exact.")
    exit(1)
  }
  return Extrait(chemin: chemin, debut: debut, fin: fin)
}

let dossier = URL(fileURLWithPath: #filePath).deletingLastPathComponent()
  .appendingPathComponent(modeFilm ? "../site/assets/media/films" : "../site/assets/media/prestations")
  .standardized
try FileManager.default.createDirectory(at: dossier, withIntermediateDirectories: true)
let sortieVideo = dossier.appendingPathComponent("\(args[0]).mp4")
let sortiePoster = dossier.appendingPathComponent("\(args[0]).jpg")
try? FileManager.default.removeItem(at: sortieVideo)

// Un plan prêt à lire : sa source, sa plage, sa place dans le montage et sa composition
// (recadrage 16:9, conversion SDR, cadence de la source).
struct Plan {
  let source: AVURLAsset; let piste: AVAssetTrack; let plage: CMTimeRange
  let decalage: CMTime; let compo: AVVideoComposition; let cadence: Double
}
var plans: [Plan] = []
var curseur = CMTime.zero
for e in extraits {
  let source = AVURLAsset(url: URL(fileURLWithPath: e.chemin))
  guard let piste = source.tracks(withMediaType: .video).first else {
    print("✗ aucune piste vidéo lisible dans : \(e.chemin)"); exit(1)
  }
  let plage = (e.debut != nil && e.fin != nil)
    ? CMTimeRange(start: CMTime(seconds: e.debut!, preferredTimescale: 600),
                  end: CMTime(seconds: e.fin!, preferredTimescale: 600))
    : piste.timeRange

  // Orientation de la source, puis remplissage du cadre 16:9 centré.
  let oriente = CGRect(origin: .zero, size: piste.naturalSize).applying(piste.preferredTransform)
  let echelle = max(rendu.width / oriente.width, rendu.height / oriente.height)
  let cadrage = piste.preferredTransform
    .concatenating(CGAffineTransform(translationX: -oriente.minX, y: -oriente.minY))
    .concatenating(CGAffineTransform(scaleX: echelle, y: echelle))
    .concatenating(CGAffineTransform(translationX: (rendu.width - oriente.width * echelle) / 2,
                                     y: (rendu.height - oriente.height * echelle) / 2))
  let couche = AVMutableVideoCompositionLayerInstruction(assetTrack: piste)
  couche.setTransform(cadrage, at: .zero)
  let instruction = AVMutableVideoCompositionInstruction()
  instruction.timeRange = CMTimeRange(start: .zero, duration: source.duration)
  instruction.layerInstructions = [couche]

  // Cadence de la source (durée d'image exacte, 1001/24000 pour du 23,976…), doublée au-delà de 30 i/s.
  var duree = piste.minFrameDuration
  if !duree.isValid || duree.seconds <= 0 { duree = CMTime(value: 1, timescale: 30) }
  if duree.seconds < 1.0 / 31 { duree = CMTimeMultiply(duree, multiplier: 2) }

  let compo = AVMutableVideoComposition()
  compo.renderSize = rendu
  compo.frameDuration = duree
  compo.instructions = [instruction]
  compo.colorPrimaries = AVVideoColorPrimaries_ITU_R_709_2
  compo.colorTransferFunction = AVVideoTransferFunction_ITU_R_709_2
  compo.colorYCbCrMatrix = AVVideoYCbCrMatrix_ITU_R_709_2

  plans.append(Plan(source: source, piste: piste, plage: plage, decalage: curseur, compo: compo,
                    cadence: 1 / duree.seconds))
  curseur = curseur + plage.duration
}
let dureeTotale = curseur

let couleurs = [AVVideoColorPrimariesKey: AVVideoColorPrimaries_ITU_R_709_2,
                AVVideoTransferFunctionKey: AVVideoTransferFunction_ITU_R_709_2,
                AVVideoYCbCrMatrixKey: AVVideoYCbCrMatrix_ITU_R_709_2]
let ecrivain = try AVAssetWriter(outputURL: sortieVideo, fileType: .mp4)
ecrivain.shouldOptimizeForNetworkUse = true
let entree = AVAssetWriterInput(mediaType: .video, outputSettings: [
  AVVideoCodecKey: AVVideoCodecType.h264,
  AVVideoWidthKey: LARGEUR,
  AVVideoHeightKey: HAUTEUR,
  AVVideoColorPropertiesKey: couleurs,
  AVVideoCompressionPropertiesKey: [
    AVVideoAverageBitRateKey: DEBIT,
    AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
    AVVideoAllowFrameReorderingKey: false,
    AVVideoMaxKeyFrameIntervalDurationKey: 2,
  ],
])
entree.expectsMediaDataInRealTime = false
ecrivain.add(entree)
let entreeSon: AVAssetWriterInput? = modeFilm ? AVAssetWriterInput(mediaType: .audio, outputSettings: [
  AVFormatIDKey: kAudioFormatMPEG4AAC,
  AVNumberOfChannelsKey: 2,
  AVSampleRateKey: 48_000,
  AVEncoderBitRateKey: 128_000,
]) : nil
if let entreeSon { entreeSon.expectsMediaDataInRealTime = false; ecrivain.add(entreeSon) }

ecrivain.startWriting()
ecrivain.startSession(atSourceTime: .zero)

// Recale un échantillon de sa source sur le montage : t_montage = t_source - début du plan + décalage.
func recaler(_ echantillon: CMSampleBuffer, _ p: Plan) -> CMSampleBuffer? {
  var n: CMItemCount = 0
  CMSampleBufferGetSampleTimingInfoArray(echantillon, entryCount: 0, arrayToFill: nil, entriesNeededOut: &n)
  var temps = [CMSampleTimingInfo](repeating: CMSampleTimingInfo(), count: max(n, 1))
  CMSampleBufferGetSampleTimingInfoArray(echantillon, entryCount: n, arrayToFill: &temps, entriesNeededOut: &n)
  for i in temps.indices {
    temps[i].presentationTimeStamp = temps[i].presentationTimeStamp - p.plage.start + p.decalage
    if temps[i].decodeTimeStamp.isValid {
      temps[i].decodeTimeStamp = temps[i].decodeTimeStamp - p.plage.start + p.decalage
    }
  }
  var copie: CMSampleBuffer?
  CMSampleBufferCreateCopyWithNewTiming(allocator: nil, sampleBuffer: echantillon,
                                        sampleTimingEntryCount: n, sampleTimingArray: &temps,
                                        sampleBufferOut: &copie)
  return copie
}

// Lit les plans l'un après l'autre (un seul décodeur ouvert à la fois) et les pousse dans
// l'entrée. Image et son tournent sur deux files : l'écrivain entrelace les deux pistes et
// attendrait l'une si l'autre n'avançait pas.
func pousser(_ vers: AVAssetWriterInput, son: Bool) throws {
  for p in plans {
    let lecteur = try AVAssetReader(asset: p.source)
    lecteur.timeRange = p.plage
    let sortie: AVAssetReaderOutput
    if son {
      guard let pisteSon = p.source.tracks(withMediaType: .audio).first else { continue }
      sortie = AVAssetReaderAudioMixOutput(audioTracks: [pisteSon],
                                           audioSettings: [AVFormatIDKey: kAudioFormatLinearPCM])
    } else {
      let s = AVAssetReaderVideoCompositionOutput(
        videoTracks: [p.piste],
        videoSettings: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA])
      s.videoComposition = p.compo
      sortie = s
    }
    lecteur.add(sortie)
    lecteur.startReading()
    while let echantillon = sortie.copyNextSampleBuffer() {
      guard let recale = recaler(echantillon, p) else { continue }
      while !vers.isReadyForMoreMediaData { usleep(2_000) }
      vers.append(recale)
    }
    if lecteur.status == .failed { throw lecteur.error ?? CocoaError(.fileReadUnknown) }
  }
  vers.markAsFinished()
}
let groupe = DispatchGroup()
var erreur: Error?
for (vers, son) in [(entree, false)] + (entreeSon.map { [($0, true)] } ?? []) {
  DispatchQueue.global().async(group: groupe) {
    do { try pousser(vers, son: son) } catch { erreur = error; vers.markAsFinished() }
  }
}
groupe.wait()
let fin = DispatchSemaphore(value: 0)
ecrivain.finishWriting { fin.signal() }
fin.wait()
guard erreur == nil, ecrivain.status == .completed else {
  print("✗ échec : \(erreur?.localizedDescription ?? ecrivain.error?.localizedDescription ?? "?")")
  exit(1)
}

// Poster : première image (boucle) ou image choisie (film), même recadrage et colorimétrie.
let premier = plans[0]
let instant = modeFilm
  ? premier.plage.start + CMTime(seconds: min(tempsPoster ?? dureeTotale.seconds * 0.25,
                                              premier.plage.duration.seconds - 0.1),
                                 preferredTimescale: 600)
  : premier.plage.start
let generateur = AVAssetImageGenerator(asset: premier.source)
generateur.videoComposition = premier.compo
generateur.maximumSize = rendu
generateur.requestedTimeToleranceBefore = .zero
generateur.requestedTimeToleranceAfter = .zero
let image = try generateur.copyCGImage(at: instant, actualTime: nil)
let jpeg = CGImageDestinationCreateWithURL(sortiePoster as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(jpeg, image, [kCGImageDestinationLossyCompressionQuality: 0.76] as CFDictionary)
CGImageDestinationFinalize(jpeg)

let poids = { (u: URL) in ((try? u.resourceValues(forKeys: [.fileSizeKey]).fileSize) ?? 0) / 1024 }
let cadences = Set(plans.map { String(format: "%.2f", $0.cadence) }).sorted().joined(separator: " / ")
let son = modeFilm ? ", avec son" : ""
print("✓ \(sortieVideo.lastPathComponent)  \(LARGEUR)×\(HAUTEUR)  \(plans.count) plan(s), "
      + "\(String(format: "%.1f", dureeTotale.seconds)) s, \(cadences) i/s\(son)  \(poids(sortieVideo)) Ko")
print("✓ \(sortiePoster.lastPathComponent)  \(poids(sortiePoster)) Ko")
