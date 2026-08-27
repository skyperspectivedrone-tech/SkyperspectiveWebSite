/* Calculateur de devis — tout se passe côté client.
   Prix = prix de la durée × (1 + coef. complexité) + options fixes + déplacement.
   Le déplacement vient d'un vrai calcul d'itinéraire routier, pas d'une distance à vol d'oiseau :
   adresse géocodée par l'API Adresse (adresse.data.gouv.fr, gratuite et sans clé).
   Le trajet est mesuré par OSRM (démo publique gratuite, sans clé) par défaut, ou par
   openrouteservice.org si config.routage.cle est renseignée (voir tarifs_config.py) —
   plus adapté à un trafic soutenu. Si le réseau est indisponible (aperçu hors ligne,
   page intégrée), un champ de secours prend le relais. */
(function () {
  var racine = document.getElementById("devis");
  if (!racine) return;

  var config = JSON.parse(document.getElementById("devis-config").textContent);
  var GEOCODAGE = "https://api-adresse.data.gouv.fr/search/";
  var ITINERAIRE = "https://router.project-osrm.org/route/v1/driving/";
  var ITINERAIRE_ORS = "https://api.openrouteservice.org/v2/directions/driving-car";

  var champs = {
    prestation: racine.querySelector("#dv-prestation"),
    formule: racine.querySelector("#dv-formule"),
    complexite: racine.querySelector("#dv-complexite"),
    duree: racine.querySelector("#dv-duree"),
  };
  var etapes = {};
  racine.querySelectorAll(".etape").forEach(function (n) { etapes[n.dataset.etape] = n; });
  var boutonRetour = racine.querySelector("#dv-retour");
  var boutonSuivant = racine.querySelector("#dv-suivant");
  var progression = racine.querySelector("#dv-progression");
  var formulaire = {
    prenom: racine.querySelector("#dv-prenom"),
    nom: racine.querySelector("#dv-nom"),
    email: racine.querySelector("#dv-email"),
    tel: racine.querySelector("#dv-tel"),
    type: racine.querySelector("#dv-type"),
    societe: racine.querySelector("#dv-societe"),
    date: racine.querySelector("#dv-date"),
    projet: racine.querySelector("#dv-projet"),
    autorisation: racine.querySelector("#dv-autorisation"),
    consentement: racine.querySelector("#dv-consentement"),
    botcheck: racine.querySelector("#dv-botcheck"),
  };
  var champSociete = racine.querySelector("#dv-societe-champ");
  var etatEnvoi = racine.querySelector("#dv-etat");
  var jauge = racine.querySelector("#dv-jauge");
  var adresse = racine.querySelector("#dv-adresse");
  var liste = racine.querySelector("#dv-suggestions");
  var secours = racine.querySelector("#dv-secours");
  var champKm = racine.querySelector("#dv-km");
  var cases = racine.querySelectorAll("[data-option]");
  var sortieTotal = racine.querySelector("#dv-total");
  var mention = racine.querySelector("#dv-mention");
  var bouton = racine.querySelector("#dv-envoyer");

  var lignes = {};
  racine.querySelectorAll("[data-recap]").forEach(function (n) { lignes[n.dataset.recap] = n; });

  var euros = new Intl.NumberFormat("fr-FR", {
    style: "currency", currency: "EUR", maximumFractionDigits: 2,
  });
  function km(v) { return v.toLocaleString("fr-FR", { maximumFractionDigits: 1 }) + " km"; }
  function libelle(select) {
    return select.selectedIndex > 0 ? select.options[select.selectedIndex].text : "";
  }

  /* ---------------- trajet ---------------- */

  var trajet = { etat: "vide" };   // vide | recherche | ok | erreur
  var modeSecours = false;

  function basculerSecours(raison) {
    if (modeSecours) return;
    modeSecours = true;
    secours.hidden = false;
    trajet = { etat: "erreur", raison: raison };
    calculer();
  }

  function distanceRoutiere(lon, lat) {
    var cle = config.routage && config.routage.cle;
    return cle ? distanceORS(lon, lat, cle) : distanceOSRM(lon, lat);
  }

  function distanceOSRM(lon, lat) {
    var d = config.depart;
    var url = ITINERAIRE + d.lon + "," + d.lat + ";" + lon + "," + lat
            + "?overview=false&alternatives=true";
    return fetch(url).then(function (r) { return r.json(); }).then(function (j) {
      if (j.code !== "Ok" || !j.routes || !j.routes.length) throw new Error("itinéraire introuvable");
      // itinéraire le plus court des variantes proposées
      var metres = j.routes.reduce(function (mini, r) {
        return Math.min(mini, r.distance);
      }, Infinity);
      return Math.round(metres / 100) / 10;
    });
  }

  function distanceORS(lon, lat, cle) {
    var d = config.depart;
    var url = ITINERAIRE_ORS + "?api_key=" + encodeURIComponent(cle)
            + "&start=" + d.lon + "," + d.lat + "&end=" + lon + "," + lat;
    return fetch(url).then(function (r) {
      if (!r.ok) throw new Error("itinéraire indisponible (" + r.status + ")");
      return r.json();
    }).then(function (j) {
      if (!j.routes || !j.routes.length) throw new Error("itinéraire introuvable");
      return Math.round(j.routes[0].summary.distance / 100) / 10;
    });
  }

  function choisirAdresse(suggestion) {
    adresse.value = suggestion.label;
    fermerListe();
    trajet = { etat: "recherche", label: suggestion.label };
    calculer();
    // Le calcul se lance dès l'adresse choisie, mais l'étape n'avance que si le
    // visiteur clique lui-même sur "Continuer" — jamais toute seule.
    distanceRoutiere(suggestion.lon, suggestion.lat).then(function (distance) {
      trajet = {
        etat: "ok",
        label: suggestion.label,
        departement: suggestion.departement,
        km: distance,
      };
      calculer();
    }).catch(function (e) { basculerSecours(String(e)); });
  }

  /* ---------------- autocomplétion ---------------- */

  var minuteur = null;
  var suggestions = [];
  var survol = -1;

  function fermerListe() {
    liste.hidden = true;
    liste.innerHTML = "";
    suggestions = [];
    survol = -1;
    adresse.setAttribute("aria-expanded", "false");
  }

  function afficherListe(items) {
    suggestions = items;
    survol = -1;
    if (!items.length) return fermerListe();
    liste.innerHTML = items.map(function (s, i) {
      return '<li role="option" id="dv-sug-' + i + '" data-index="' + i + '">' + s.label + "</li>";
    }).join("");
    liste.hidden = false;
    adresse.setAttribute("aria-expanded", "true");
  }

  function chercher(texte) {
    // Biais de proximité : sans lui, « place de la mairie sete » remontait un homonyme
    // dans l'Aube avant Sète. L'API classe les résultats par distance au point donné.
    var d = config.depart;
    fetch(GEOCODAGE + "?q=" + encodeURIComponent(texte)
          + "&limit=5&autocomplete=1&lat=" + d.lat + "&lon=" + d.lon)
      .then(function (r) { return r.json(); })
      .then(function (j) {
        afficherListe((j.features || []).map(function (f) {
          return {
            label: f.properties.label,
            lon: f.geometry.coordinates[0],
            lat: f.geometry.coordinates[1],
            departement: (f.properties.postcode || "").slice(0, 2),
          };
        }));
      })
      .catch(function (e) { basculerSecours(String(e)); });
  }

  if (adresse) {
    adresse.addEventListener("input", function () {
      trajet = { etat: "vide" };
      calculer();
      window.clearTimeout(minuteur);
      var texte = adresse.value.trim();
      if (texte.length < 3) return fermerListe();
      minuteur = window.setTimeout(function () { chercher(texte); }, 300);
    });

    adresse.addEventListener("keydown", function (e) {
      if (liste.hidden) return;
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        survol += e.key === "ArrowDown" ? 1 : -1;
        if (survol < 0) survol = suggestions.length - 1;
        if (survol >= suggestions.length) survol = 0;
        liste.querySelectorAll("li").forEach(function (li, i) {
          li.classList.toggle("is-survol", i === survol);
        });
      } else if (e.key === "Enter" && survol >= 0) {
        e.preventDefault();
        choisirAdresse(suggestions[survol]);
      } else if (e.key === "Escape") {
        fermerListe();
      }
    });

    liste.addEventListener("mousedown", function (e) {
      var li = e.target.closest("li[data-index]");
      if (li) { e.preventDefault(); choisirAdresse(suggestions[+li.dataset.index]); }
    });

    document.addEventListener("click", function (e) {
      if (!racine.contains(e.target)) fermerListe();
    });
  }

  if (champKm) champKm.addEventListener("input", calculer);

  /* ---------------- menus dépendants ---------------- */

  function majMenusDependants() {
    var p = config.prestations[champs.prestation.value];

    var formules = p && p.formules;
    if (formules) {
      var attendu = formules.map(function (f) { return f.cle; }).join(",");
      if (champs.formule.dataset.pour !== attendu) {
        champs.formule.dataset.pour = attendu;
        champs.formule.innerHTML = '<option value="">Sélectionnez…</option>'
          + formules.map(function (f) {
              return '<option value="' + f.cle + '">' + f.libelle + "</option>";
            }).join("");
      }
    } else {
      champs.formule.value = "";
    }
    if (!(p && p.duree)) champs.duree.value = "";
    majOptionsImposees();
  }

  /* ---------------- options imposées ---------------- */

  function majOptionsImposees() {
    var cle = champs.prestation.value;
    cases.forEach(function (c) {
      var concernees = config.optionsImposees[c.dataset.option];
      var impose = !!(concernees && concernees.indexOf(cle) !== -1);
      var etiquette = c.closest(".case");
      etiquette.classList.toggle("is-verrouille", impose);
      if (impose) {
        if (!c.checked) c.dataset.auto = "1";   // cochée par la prestation, pas par le visiteur
        c.checked = true;
        c.setAttribute("aria-disabled", "true");
      } else {
        c.removeAttribute("aria-disabled");
        // On ne relâche que ce qui avait été coché automatiquement.
        if (c.dataset.auto === "1") { c.checked = false; delete c.dataset.auto; }
      }
    });
  }

  // Une option imposée ne peut pas être décochée par le visiteur.
  cases.forEach(function (c) {
    c.addEventListener("click", function (e) {
      if (c.getAttribute("aria-disabled") === "true") { e.preventDefault(); c.checked = true; }
    });
  });

  // Bulles d'explication
  racine.querySelectorAll(".info").forEach(function (b) {
    var bulle = document.getElementById(b.getAttribute("aria-controls"));
    b.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      var ouvert = b.getAttribute("aria-expanded") === "true";
      b.setAttribute("aria-expanded", String(!ouvert));
      bulle.hidden = ouvert;
    });
    document.addEventListener("click", function (e) {
      if (!bulle.hidden && !bulle.contains(e.target) && e.target !== b) {
        bulle.hidden = true;
        b.setAttribute("aria-expanded", "false");
      }
    });
  });

  /* ---------------- parcours par étapes ---------------- */

  var ORDRE = ["prestation", "formule", "adresse", "complexite", "duree", "options",
               "coordonnees", "fin"];
  var position = 0;

  function applicable(cle) {
    var p = config.prestations[champs.prestation.value];
    if (cle === "formule") return !!(p && p.formules);
    if (cle === "duree") return !!(p && p.duree);
    return true;
  }

  function parcours() { return ORDRE.filter(applicable); }

  function repondue(cle) {
    if (cle === "prestation") return !!champs.prestation.value;
    if (cle === "formule") return !!champs.formule.value;
    if (cle === "complexite") return !!champs.complexite.value;
    if (cle === "duree") return !!champs.duree.value;
    // L'adresse n'est jamais bloquante : sans elle, le déplacement reste « à préciser »
    // plutôt que d'enfermer le visiteur dans l'étape.
    if (cle === "adresse") return true;
    if (cle === "coordonnees") return formulaireValide();
    return true;   // options et fin : toujours franchissables
  }

  function pro() {
    return formulaire.type.value && formulaire.type.value !== "particulier";
  }

  function formulaireValide() {
    if (!formulaire.prenom.value.trim()) return false;
    if (!formulaire.nom.value.trim()) return false;
    if (!formulaire.email.checkValidity() || !formulaire.email.value.trim()) return false;
    if (!formulaire.tel.value.trim()) return false;
    if (!formulaire.type.value) return false;
    if (pro() && !formulaire.societe.value.trim()) return false;
    if (!formulaire.autorisation.checked) return false;
    if (!formulaire.consentement.checked) return false;
    return true;
  }

  var sondeFaite = false;

  function verifierDisponibilite() {
    if (sondeFaite || modeSecours) return;
    sondeFaite = true;
    fetch(GEOCODAGE + "?q=montpellier&limit=1")
      .then(function (r) { if (!r.ok) throw new Error("service indisponible"); })
      .catch(function (e) { basculerSecours(String(e)); });
  }

  var etapeAffichee = null;

  function afficherEtape() {
    var liste = parcours();
    if (position >= liste.length) position = liste.length - 1;
    if (position < 0) position = 0;
    var courante = liste[position];
    // On ne force le focus que lors d'une vraie transition vers cette étape,
    // jamais quand afficherEtape() est relancé par une simple frappe dans un
    // champ déjà affiché (formulaire de coordonnées) — sinon le focus revient
    // sans arrêt sur le premier champ (prénom) à chaque caractère tapé ailleurs.
    var changementEtape = courante !== etapeAffichee;
    etapeAffichee = courante;

    ORDRE.forEach(function (cle) {
      if (etapes[cle]) etapes[cle].hidden = cle !== courante;
    });

    boutonRetour.hidden = position === 0;
    var derniere = courante === "fin";
    // L'envoi se fait uniquement depuis le bouton du récapitulatif : un second
    // bouton "Envoyer ma demande" ici ferait doublon.
    boutonSuivant.hidden = derniere || courante === "coordonnees";
    if (courante === "coordonnees") champSociete.hidden = !pro();
    boutonSuivant.disabled = !repondue(courante);

    var etapesChiffrees = liste.length - 1;   // « fin » ne compte pas
    var numero = Math.min(position + 1, etapesChiffrees);
    progression.textContent = derniere
      ? "Terminé"
      : "Étape " + numero + " sur " + etapesChiffrees;
    jauge.style.width = Math.round(((derniere ? etapesChiffrees : position) / etapesChiffrees) * 100) + "%";

    if (courante === "adresse") verifierDisponibilite();
    majBoutonEnvoi();

    if (changementEtape) {
      var champ = etapes[courante] && etapes[courante].querySelector("select, input");
      if (champ && courante !== "prestation") {
        window.setTimeout(function () { champ.focus({ preventScroll: true }); }, 0);
      }
    }
  }

  function avancer() {
    var liste = parcours();
    if (!repondue(liste[position])) return;
    if (position < liste.length - 1) position += 1;
    afficherEtape();
  }

  boutonSuivant.addEventListener("click", avancer);
  boutonRetour.addEventListener("click", function () {
    if (position > 0) position -= 1;
    afficherEtape();
  });

  /* ---------------- calcul ---------------- */

  function deplacement() {
    if (modeSecours) {
      var saisi = parseFloat(champKm.value);
      if (isNaN(saisi) || saisi < 0) return { etat: "vide" };
      if (saisi <= config.seuilKm) return { etat: "inclus", km: saisi };
      var t = saisi * (config.allerRetour ? 2 : 1);
      return { etat: "calcule", km: saisi, montant: t * config.prixKm };
    }
    if (trajet.etat === "vide") return { etat: "vide" };
    if (trajet.etat === "recherche") return { etat: "recherche" };
    if (trajet.etat !== "ok") return { etat: "vide" };
    if (trajet.km <= config.seuilKm) return { etat: "inclus", km: trajet.km };
    if (trajet.departement && trajet.departement !== config.departement) {
      return { etat: "adeterminer", km: trajet.km };
    }
    var factures = trajet.km * (config.allerRetour ? 2 : 1);
    return { etat: "calcule", km: trajet.km, montant: factures * config.prixKm };
  }

  function calculer() {
    majMenusDependants();
    if (typeof boutonSuivant !== "undefined" && !boutonSuivant.hidden) {
      var liste = parcours();
      boutonSuivant.disabled = !repondue(liste[Math.min(position, liste.length - 1)]);
    }

    var prestation = config.prestations[champs.prestation.value];
    var formule = null;
    if (prestation && prestation.formules && champs.formule.value) {
      formule = prestation.formules.filter(function (f) {
        return f.cle === champs.formule.value;
      })[0] || null;
    }

    var prixPrestation = null;
    if (prestation) {
      if (prestation.formules) prixPrestation = formule ? formule.prix : null;
      else prixPrestation = prestation.base;
    }

    var cleDuree = champs.duree.value;
    var avecDuree = !!(prestation && prestation.duree);
    var supplementDuree = avecDuree && cleDuree ? config.durees[cleDuree] : 0;

    var cleComplexite = champs.complexite.value;
    var coefComplexite = cleComplexite ? config.complexites[cleComplexite] : null;
    var dep = deplacement();

    // ---- récapitulatif ----
    if (!prestation) {
      lignes.prestation.textContent = "—";
    } else {
      var texte = libelle(champs.prestation);
      if (formule) texte += " — " + formule.libelle;
      if (typeof prixPrestation === "number") {
        texte += " · " + (formule && formule.apartir ? "à partir de " : "")
               + euros.format(prixPrestation);
      } else if (prestation.formules) {
        texte += " — choisissez une formule";
      }
      lignes.prestation.textContent = texte;
    }

    lignes.complexite.textContent = cleComplexite
      ? libelle(champs.complexite) + (coefComplexite ? " · + " + Math.round(coefComplexite * 100) + " %" : "")
      : "—";

    if (!avecDuree) {
      lignes.duree.textContent = prestation ? "Comprise dans la prestation" : "—";
    } else if (!cleDuree) {
      lignes.duree.textContent = "—";
    } else if (supplementDuree === null) {
      lignes.duree.textContent = libelle(champs.duree) + " · sur devis";
    } else if (supplementDuree === 0) {
      lignes.duree.textContent = libelle(champs.duree) + " · comprise";
    } else {
      lignes.duree.textContent = libelle(champs.duree) + " · + " + euros.format(supplementDuree);
    }

    var libellesOptions = [];
    var optionsFixes = 0;
    var optionsSurDevis = false;
    cases.forEach(function (c) {
      if (!c.checked) return;
      var o = config.options[c.dataset.option];
      if (o && typeof o.prix === "number") {
        optionsFixes += o.prix;
        libellesOptions.push(c.dataset.libelle + " · + " + euros.format(o.prix));
      } else {
        optionsSurDevis = true;
        libellesOptions.push(c.dataset.libelle + " · sur devis");
      }
    });
    lignes.options.textContent = libellesOptions.length ? libellesOptions.join(" — ") : "Aucune";

    lignes.deplacement.classList.remove("is-gratuit");
    if (dep.etat === "vide") {
      lignes.deplacement.textContent = position > 0 ? "À préciser" : "—";
    } else if (dep.etat === "recherche") {
      lignes.deplacement.textContent = "Calcul du trajet…";
    } else if (dep.etat === "inclus") {
      lignes.deplacement.textContent = dep.km < 1 ? "Inclus" : km(dep.km) + " — inclus";
      lignes.deplacement.classList.add("is-gratuit");
    } else if (dep.etat === "adeterminer") {
      lignes.deplacement.textContent = km(dep.km) + " — à déterminer";
    } else {
      lignes.deplacement.textContent = km(dep.km) + " · " + euros.format(dep.montant);
    }

    // ---- total ----
    var pretPrestation = typeof prixPrestation === "number";
    var pretDuree = !avecDuree || !!cleDuree;
    if (!pretPrestation || !cleComplexite || !pretDuree) {
      sortieTotal.textContent = "—";
      mention.textContent = "Renseignez la prestation"
        + (prestation && prestation.formules ? ", la formule" : "")
        + (avecDuree ? ", la durée" : "")
        + " et la complexité pour obtenir une estimation.";
      bouton.setAttribute("aria-disabled", "true");
      return;
    }
    bouton.removeAttribute("aria-disabled");

    var reserves = [];
    var sousTotal = prixPrestation;
    if (supplementDuree === null) {
      reserves.push("une prestation de plus d’une journée est chiffrée sur devis : ce montant "
                  + "ne comprend que la première journée");
    } else {
      sousTotal += supplementDuree;
    }
    if (formule && formule.apartir) {
      reserves.push("cette inspection est facturée à partir de "
                  + euros.format(formule.prix) + ", selon l’ouvrage à couvrir");
    }

    var total = sousTotal * (1 + coefComplexite) + optionsFixes;
    if (optionsSurDevis) {
      reserves.push("les options marquées « sur devis » seront chiffrées après étude");
    }
    if (dep.etat === "calcule") total += dep.montant;
    if (dep.etat === "adeterminer") {
      reserves.push("le déplacement hors Hérault n’est pas compris : je le fixe au cas par cas, "
                  + "selon le trajet le plus économique");
    }
    if (dep.etat === "vide") {
      reserves.push("le déplacement n’est pas compris, faute d’adresse renseignée");
    }

    sortieTotal.textContent = euros.format(total);
    mention.textContent = (reserves.length ? "Attention, " + reserves.join(" ; ") + ". " : "")
      + "Estimation indicative, établie sur la base des informations fournies. "
      + "Un devis précis vous est adressé après étude du projet.";

    majBoutonEnvoi();
  }

  // Une fois sur l'étape des coordonnées, le bouton du récapitulatif devient
  // l'envoi réel : il reste désactivé tant que le formulaire n'est pas complet.
  function majBoutonEnvoi() {
    if (parcours()[Math.min(position, parcours().length - 1)] !== "coordonnees") return;
    if (formulaireValide()) bouton.removeAttribute("aria-disabled");
    else bouton.setAttribute("aria-disabled", "true");
  }

  // Choisir une option met à jour le calcul et débloque "Continuer" (le nombre
  // total d'étapes peut aussi changer selon la prestation), mais c'est toujours
  // au visiteur de cliquer pour passer à l'étape suivante.
  Object.keys(champs).forEach(function (k) {
    champs[k].addEventListener("change", function () { calculer(); afficherEtape(); });
  });
  cases.forEach(function (c) { c.addEventListener("change", calculer); });

  Object.keys(formulaire).forEach(function (k) {
    var champ = formulaire[k];
    if (!champ) return;
    ["input", "change"].forEach(function (evt) {
      champ.addEventListener(evt, function () {
        if (k === "type") champSociete.hidden = !pro();
        afficherEtape();
        majBoutonEnvoi();
      });
    });
  });

  /* ---------------- envoi de la demande ---------------- */

  function resume() {
    var l = [];
    racine.querySelectorAll("[data-recap]").forEach(function (n) {
      var libelle = n.parentNode.querySelector("span").textContent;
      l.push(libelle + " : " + n.textContent);
    });
    l.push("Adresse du tournage : " + (adresse.value || "non précisée"));
    l.push("Total estimatif : " + sortieTotal.textContent);
    return l.join("\n");
  }

  function messageTexte() {
    var f = formulaire;
    return [
      f.prenom.value + " " + f.nom.value
        + (pro() ? " — " + f.societe.value : " (particulier)"),
      "Téléphone : " + f.tel.value,
      "E-mail : " + f.email.value,
      "Date souhaitée : " + (f.date.value || "non précisée"),
      "",
      "Projet :",
      f.projet.value || "(non renseigné)",
      "",
      "--- Estimation calculée sur le site ---",
      resume(),
    ].join("\n");
  }

  function lienSecours() {
    return "mailto:" + bouton.dataset.email
      + "?subject=" + encodeURIComponent("Demande de devis — " + libelle(champs.prestation))
      + "&body=" + encodeURIComponent(messageTexte());
  }

  function etat(texte, type) {
    etatEnvoi.textContent = texte;
    etatEnvoi.className = "formulaire__etat" + (type ? " is-" + type : "");
  }

  function envoyer() {
    if (!formulaireValide()) return;
    if (formulaire.botcheck.checked) return;          // piège à robots

    var cle = config.formulaire && config.formulaire.cle;
    if (!cle) {
      etat("L’envoi automatique n’est pas encore configuré : votre messagerie va s’ouvrir "
         + "avec la demande déjà rédigée.", "info");
      window.location.href = lienSecours();
      return;
    }

    bouton.setAttribute("aria-disabled", "true");
    etat("Envoi en cours…", "info");

    // La documentation impose du JSON pour les appels en JavaScript,
    // pas du multipart ni de l'urlencoded.
    var donnees = {
      access_key: cle,
      subject: "Demande de devis — " + libelle(champs.prestation),
      from_name: "Site Sky Perspective",
      name: formulaire.prenom.value + " " + formulaire.nom.value,
      email: formulaire.email.value,
      message: messageTexte(),
    };

    fetch(config.formulaire.endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(donnees),
    })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.success) throw new Error(j.message || "envoi refusé");
        etat("", null);              // sinon « Envoi en cours… » reste affiché au retour
        position = parcours().indexOf("fin");
        afficherEtape();
      })
      .catch(function (e) {
        bouton.removeAttribute("aria-disabled");
        etat("L’envoi a échoué (" + e.message + "). Votre messagerie va s’ouvrir avec la "
           + "demande déjà rédigée.", "erreur");
        window.setTimeout(function () { window.location.href = lienSecours(); }, 1200);
      });
  }

  // Bouton unique du récapitulatif : avant l'étape des coordonnées, il y conduit ;
  // une fois dessus, il envoie réellement la demande (pas de second bouton en doublon
  // dans le pied de l'étape).
  bouton.addEventListener("click", function (e) {
    e.preventDefault();
    var liste = parcours();
    var cible = liste.indexOf("coordonnees");
    if (cible >= 0 && position < cible) { position = cible; afficherEtape(); return; }
    if (liste[position] === "coordonnees") envoyer();
  });

  calculer();
  afficherEtape();

  /* ---------------- curseur visuel pour la durée ---------------- */
  /* Amélioration purement visuelle : le <select> #dv-duree reste la
     source de vérité et continue de piloter tout le calcul ci-dessus. */
  (function curseurDuree() {
    var select = champs.duree;
    if (!select) return;
    var options = Array.prototype.slice.call(select.options).filter(function (o) { return o.value; });
    if (!options.length) return;

    select.classList.add('sr-only');
    var bloc = document.createElement('div');
    bloc.className = 'slider';
    bloc.innerHTML =
      '<div class="slider__head"><span class="slider__value" id="dv-duree-valeur"></span></div>' +
      '<div class="slider__track">' +
        '<div class="slider__rail"></div><div class="slider__fill" id="dv-duree-remplissage"></div>' +
        '<div class="slider__thumb" id="dv-duree-curseur"></div>' +
        '<input type="range" id="dv-duree-range" min="0" max="' + (options.length - 1) + '" step="1" value="0">' +
      '</div>';
    select.insertAdjacentElement('afterend', bloc);

    var range = bloc.querySelector('#dv-duree-range');
    var valeur = bloc.querySelector('#dv-duree-valeur');
    var remplissage = bloc.querySelector('#dv-duree-remplissage');
    var curseur = bloc.querySelector('#dv-duree-curseur');

    function dessiner() {
      var i = Number(range.value);
      var pct = options.length > 1 ? (i / (options.length - 1)) * 100 : 0;
      remplissage.style.width = pct + '%';
      curseur.style.left = pct + '%';
      valeur.textContent = options[i].text;
    }
    function versSelect() {
      // Ne PAS déclencher l'évènement "change" du select ici : c'est lui qui fait
      // avancer automatiquement à l'étape suivante ailleurs dans ce fichier. Le
      // visiteur doit pouvoir glisser librement et valider lui-même sur "Continuer".
      select.value = options[Number(range.value)].value;
      calculer();
      dessiner();
    }
    function depuisSelect() {
      var i = options.findIndex(function (o) { return o.value === select.value; });
      range.value = String(Math.max(0, i));
      dessiner();
    }
    range.addEventListener('input', versSelect);
    var origine = majMenusDependants;
    majMenusDependants = function () { origine(); depuisSelect(); };
    depuisSelect();
  })();
})();
