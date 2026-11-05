// Prépare les vidéos web de la page Prestations, en H.264 1280 × 720 à 30 i/s, démarrage
// rapide (faststart), plus une image d'attente (poster) en JPEG.
//
// Deux usages :
//  - boucle (défaut) : plusieurs extraits enchaînés en coupes franches, SANS son, ~1,8 Mbit/s.
//    Le poster est la première image, pour que le passage poster → vidéo ne saute pas.
//        swift -suppress-warnings _build/video_prestation.swift <id> <source>:<debut>-<fin> [...]
//    → site/assets/media/prestations/<id>.mp4 et <id>.jpg
//  - film (--film) : une vidéo source entière, AVEC son (AAC 128 kbit/s), ~3 Mbit/s.
//        swift -suppress-warnings _build/video_prestation.swift --film [--poster <s>] <id> <source>
//    → site/assets/media/films/<id>.mp4 et <id>.jpg (poster pris à <s> secondes, 25 % par défaut)
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
let DEBIT = modeFilm ? 3_000_000 : 1_800_000
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

// Montage : les extraits bout à bout sur une piste image (et une piste son en mode film),
// chacun avec son recadrage.
let montage = AVMutableComposition()
let piste = montage.addMutableTrack(withMediaType: .video, preferredTrackID: kCMPersistentTrackID_Invalid)!
let pisteSon = modeFilm
  ? montage.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid) : nil
var curseur = CMTime.zero
var instructions: [AVMutableVideoCompositionInstruction] = []
for e in extraits {
  let source = AVURLAsset(url: URL(fileURLWithPath: e.chemin))
  guard let pisteSource = source.tracks(withMediaType: .video).first else {
    print("✗ aucune piste vidéo lisible dans : \(e.chemin)"); exit(1)
  }
  let plage = (e.debut != nil && e.fin != nil)
    ? CMTimeRange(start: CMTime(seconds: e.debut!, preferredTimescale: 600),
                  end: CMTime(seconds: e.fin!, preferredTimescale: 600))
    : pisteSource.timeRange
  try piste.insertTimeRange(plage, of: pisteSource, at: curseur)
  if let pisteSon {
    if let sonSource = source.tracks(withMediaType: .audio).first {
      try pisteSon.insertTimeRange(plage, of: sonSource, at: curseur)
    } else {
      pisteSon.insertEmptyTimeRange(CMTimeRange(start: curseur, duration: plage.duration))
    }
  }

  // Orientation de la source, puis remplissage du cadre 16:9 centré.
  let oriente = CGRect(origin: .zero, size: pisteSource.naturalSize).applying(pisteSource.preferredTransform)
  let echelle = max(rendu.width / oriente.width, rendu.height / oriente.height)
  let cadrage = pisteSource.preferredTransform
    .concatenating(CGAffineTransform(translationX: -oriente.minX, y: -oriente.minY))
    .concatenating(CGAffineTransform(scaleX: echelle, y: echelle))
    .concatenating(CGAffineTransform(translationX: (rendu.width - oriente.width * echelle) / 2,
                                     y: (rendu.height - oriente.height * echelle) / 2))
  let couche = AVMutableVideoCompositionLayerInstruction(assetTrack: piste)
  couche.setTransform(cadrage, at: curseur)
  let instruction = AVMutableVideoCompositionInstruction()
  instruction.timeRange = CMTimeRange(start: curseur, duration: plage.duration)
  instruction.layerInstructions = [couche]
  instructions.append(instruction)
  curseur = curseur + plage.duration
}
// La dernière instruction doit finir exactement avec la piste image, sinon la composition est refusée.
if let derniere = instructions.last {
  derniere.timeRange = CMTimeRange(start: derniere.timeRange.start, end: piste.timeRange.end)
}

let compo = AVMutableVideoComposition()
compo.renderSize = rendu
compo.frameDuration = CMTime(value: 1, timescale: 30)
compo.instructions = instructions
compo.colorPrimaries = AVVideoColorPrimaries_ITU_R_709_2
compo.colorTransferFunction = AVVideoTransferFunction_ITU_R_709_2
compo.colorYCbCrMatrix = AVVideoYCbCrMatrix_ITU_R_709_2

let lecteur = try AVAssetReader(asset: montage)
lecteur.timeRange = CMTimeRange(start: .zero, end: piste.timeRange.end)
let sortie = AVAssetReaderVideoCompositionOutput(
  videoTracks: [piste],
  videoSettings: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA])
sortie.videoComposition = compo
lecteur.add(sortie)
let sortieSon = pisteSon.map {
  AVAssetReaderAudioMixOutput(audioTracks: [$0], audioSettings: [AVFormatIDKey: kAudioFormatLinearPCM])
}
if let sortieSon { lecteur.add(sortieSon) }

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
    AVVideoMaxKeyFrameIntervalKey: 60,
  ],
])
entree.expectsMediaDataInRealTime = false
ecrivain.add(entree)
let entreeSon = sortieSon.map { _ in
  AVAssetWriterInput(mediaType: .audio, outputSettings: [
    AVFormatIDKey: kAudioFormatMPEG4AAC,
    AVNumberOfChannelsKey: 2,
    AVSampleRateKey: 48_000,
    AVEncoderBitRateKey: 128_000,
  ])
}
if let entreeSon { entreeSon.expectsMediaDataInRealTime = false; ecrivain.add(entreeSon) }

lecteur.startReading()
ecrivain.startWriting()
ecrivain.startSession(atSourceTime: .zero)
let groupe = DispatchGroup()
func copier(_ de: AVAssetReaderOutput, vers: AVAssetWriterInput, file: String) {
  groupe.enter()
  vers.requestMediaDataWhenReady(on: DispatchQueue(label: file)) {
    while vers.isReadyForMoreMediaData {
      if let echantillon = de.copyNextSampleBuffer() {
        vers.append(echantillon)
      } else {
        vers.markAsFinished()
        groupe.leave()
        return
      }
    }
  }
}
copier(sortie, vers: entree, file: "image")
if let sortieSon, let entreeSon { copier(sortieSon, vers: entreeSon, file: "son") }
groupe.wait()
let fin = DispatchSemaphore(value: 0)
ecrivain.finishWriting { fin.signal() }
fin.wait()
guard ecrivain.status == .completed else {
  print("✗ échec : \(ecrivain.error?.localizedDescription ?? lecteur.error?.localizedDescription ?? "?")")
  exit(1)
}

// Poster : première image (boucle) ou image choisie (film), même recadrage et colorimétrie.
let duree = CMTimeGetSeconds(piste.timeRange.end)
let instantPoster = modeFilm ? min(tempsPoster ?? duree * 0.25, duree - 0.1) : 0
let generateur = AVAssetImageGenerator(asset: montage)
generateur.videoComposition = compo
generateur.maximumSize = rendu
generateur.requestedTimeToleranceBefore = .zero
generateur.requestedTimeToleranceAfter = .zero
let image = try generateur.copyCGImage(at: CMTime(seconds: instantPoster, preferredTimescale: 600), actualTime: nil)
let jpeg = CGImageDestinationCreateWithURL(sortiePoster as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(jpeg, image, [kCGImageDestinationLossyCompressionQuality: 0.76] as CFDictionary)
CGImageDestinationFinalize(jpeg)

let poids = { (u: URL) in ((try? u.resourceValues(forKeys: [.fileSizeKey]).fileSize) ?? 0) / 1024 }
let son = modeFilm ? ", avec son" : ""
print("✓ \(sortieVideo.lastPathComponent)  \(LARGEUR)×\(HAUTEUR)  \(extraits.count) plan(s), \(String(format: "%.1f", duree)) s\(son)  \(poids(sortieVideo)) Ko")
print("✓ \(sortiePoster.lastPathComponent)  \(poids(sortiePoster)) Ko")
