# -*- coding: utf-8 -*-
"""Mentions légales et politique de confidentialité."""
import p_realisations
from layout import SITE


def _bloc(titre, corps):
    return f"""<div class="legal-block reveal-in">
          <h2 class="legal-block__title">{titre}</h2>
          <div class="legal-block__body">{corps}</div>
        </div>"""


def _page(eyebrow, titre, lead, blocs):
    return f"""    <section class="page-hero">
      <div class="container reveal-in">
        <p class="eyebrow">{eyebrow}</p>
        <h1 class="page-hero__title">{titre}</h1>
        <p class="page-hero__lead">{lead}</p>
      </div>
    </section>
    <section class="section" style="padding-top:0"><div class="container">
{blocs}
    </div></section>"""


def mentions_legales():
    blocs = "\n".join([
        _bloc("Éditeur du site", f"""
          <p>{SITE['nom']}, entreprise individuelle (micro-entreprise).<br>
          SIRET : {SITE['siret']}<br>
          Siège : {SITE['ville']}<br>
          Téléphone : {SITE['tel']}<br>
          E-mail : <a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
          <p style="margin-top:14px">Directeur de la publication : le gérant de {SITE['nom']}.</p>"""),
        _bloc("Hébergement", """
          <p>Le site est hébergé par GitHub Pages — GitHub, Inc.,
          88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>"""),
        _bloc("Activité et assurance", """
          <p>Exploitant d’aéronef sans équipage à bord (UAS) enregistré auprès de la
          Direction générale de l’aviation civile. Les vols sont réalisés dans le respect
          du règlement européen applicable aux opérations de drones et des restrictions
          d’espace aérien en vigueur. Une assurance responsabilité civile professionnelle
          couvre l’ensemble des missions.</p>"""),
        _bloc("Propriété intellectuelle", f"""
          <p>L’ensemble des contenus présents sur ce site — textes, photographies,
          séquences vidéo, modèles 3D, identité visuelle — est la propriété exclusive de
          {SITE['nom']}, sauf mention contraire. Toute reproduction ou diffusion, totale
          ou partielle, sans autorisation écrite préalable est interdite.</p>
          <p style="margin-top:14px">Les images livrées aux clients font l’objet d’une
          cession de droits dont l’étendue — support, durée, territoire — est précisée au devis.</p>"""),
        _bloc("Responsabilité", """
          <p>Les informations publiées sur ce site sont fournies à titre indicatif. Les
          estimations issues du calculateur de devis ne constituent pas une offre
          contractuelle : seul un devis écrit et signé engage les parties.</p>"""),
    ])
    return _page("Informations légales", "Mentions légales",
                 "Informations relatives à l’éditeur, à l’hébergement et aux conditions "
                 "d’utilisation de ce site.", blocs)


def confidentialite():
    blocs = "\n".join([
        _bloc("Données collectées", f"""
          <p>Ce site ne dépose aucun cookie de mesure d’audience ni de publicité.</p>
          <p style="margin-top:14px">Les seules données personnelles traitées sont celles que
          vous transmettez volontairement lors d’une demande de devis ou d’un message :
          nom, adresse e-mail, téléphone, et les éléments décrivant votre projet. Elles sont
          utilisées uniquement pour répondre à votre demande et établir une proposition
          commerciale.</p>"""),
        _bloc("Traitement du formulaire", """
          <p>La demande de devis est acheminée par le service <strong>Web3Forms</strong>, qui
          transmet le contenu du formulaire par courrier électronique sans le conserver à des
          fins commerciales. Aucune inscription ni aucun cookie n’est requis de votre part.</p>"""),
        *([_bloc("Vidéos intégrées", """
          <p>Les vidéos de la page Réalisations sont hébergées sur <strong>YouTube</strong>,
          en mode de confidentialité renforcée. Aucun contenu YouTube n’est chargé tant que
          vous ne cliquez pas sur une vidéo ; c’est seulement à ce moment que YouTube peut
          déposer ses propres cookies.</p>""")] if p_realisations.a_des_videos() else []),
        _bloc("Conservation et destinataires", f"""
          <p>Les demandes sans suite sont conservées douze mois. Les données liées à une
          prestation réalisée sont conservées le temps requis par les obligations comptables.</p>
          <p style="margin-top:14px">Aucune donnée n’est vendue ni transmise à des tiers à des
          fins commerciales. Seul {SITE['nom']} y a accès.</p>"""),
        _bloc("Vos droits", f"""
          <p>Conformément au Règlement général sur la protection des données, vous disposez
          d’un droit d’accès, de rectification, d’effacement, de limitation et d’opposition
          sur vos données. Pour l’exercer, écrivez à
          <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>
          <p style="margin-top:14px">Vous pouvez également introduire une réclamation auprès
          de la CNIL, autorité de contrôle française.</p>"""),
        _bloc("Prises de vue et droit à l’image", """
          <p>Les tournages sont réalisés de manière à éviter la captation de personnes
          identifiables et de propriétés privées tierces. Lorsque cela n’est pas possible,
          les autorisations nécessaires sont recueillies auprès des personnes concernées ou
          les images sont floutées. Toute personne apparaissant sur une image diffusée peut
          en demander le retrait.</p>"""),
    ])
    return _page("Protection des données", "Confidentialité",
                 "Comment vos données sont collectées, utilisées et protégées lorsque vous "
                 "me contactez.", blocs)
