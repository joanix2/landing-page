"""Service d'envoi d'emails avec gestion des templates Jinja2."""

import smtplib
import ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Dict, Any
import os
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class EmailService:
    """Service pour l'envoi d'emails via SMTP avec templates Jinja2."""
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.hostinger.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SMTP_EMAIL", "contact@axynis.cloud")
        self.password = os.getenv("SMTP_PASSWORD")
        
        # Configuration de Jinja2
        template_dir = Path(__file__).parent / "templates"
        self.jinja_env = Environment(loader=FileSystemLoader(str(template_dir)))
        
        if not self.password:
            print("⚠️  SMTP_PASSWORD non défini dans .env")
    
    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Rend un template Jinja2 avec le contexte fourni.
        
        Args:
            template_name: Nom du fichier template
            context: Dictionnaire de variables pour le template
            
        Returns:
            str: Template rendu
        """
        template = self.jinja_env.get_template(template_name)
        return template.render(**context)
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None
    ) -> bool:
        """
        Envoie un email simple.
        
        Args:
            to_email: Email du destinataire
            subject: Sujet de l'email
            body_text: Corps de l'email en texte brut
            body_html: Corps de l'email en HTML (optionnel)
            
        Returns:
            bool: True si l'email a été envoyé avec succès
        """
        try:
            # Créer le message
            if body_html:
                msg = MIMEMultipart("alternative")
                msg["From"] = self.sender_email
                msg["To"] = to_email
                msg["Subject"] = subject
                
                # Ajouter les deux versions
                part1 = MIMEText(body_text, "plain")
                part2 = MIMEText(body_html, "html")
                msg.attach(part1)
                msg.attach(part2)
            else:
                msg = EmailMessage()
                msg["From"] = self.sender_email
                msg["To"] = to_email
                msg["Subject"] = subject
                msg.set_content(body_text)
            
            # Envoyer via SMTP
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.password)
                server.send_message(msg)
            
            print(f"✅ Email envoyé à {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de l'envoi de l'email à {to_email}: {e}")
            return False
    
    def send_newsletter_confirmation(self, email: str) -> bool:
        """
        Envoie un email de confirmation d'abonnement à la newsletter.
        
        Args:
            email: Email du destinataire
            
        Returns:
            bool: True si l'email a été envoyé avec succès
        """
        subject = "✅ Confirmation d'abonnement à la newsletter Axynis"
        
        context = {
            "email": email,
            "year": datetime.now().year
        }
        
        body_text = self.render_template("newsletter_confirmation.txt", context)
        body_html = self.render_template("newsletter_confirmation.html", context)
        
        return self.send_email(email, subject, body_text, body_html)
    
    def send_estimation_confirmation(
        self,
        email: str,
        client_data: Dict[str, Any],
        estimation_data: Dict[str, Any]
    ) -> bool:
        """
        Envoie un email de confirmation de demande d'estimation.
        
        Args:
            email: Email du destinataire
            client_data: Données du client
            estimation_data: Données de l'estimation
            
        Returns:
            bool: True si l'email a été envoyé avec succès
        """
        subject = "✅ Demande d'estimation reçue - Axynis"
        
        context = {
            "client": client_data,
            "estimation": estimation_data,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "year": datetime.now().year
        }
        
        body_text = self.render_template("estimation_confirmation.txt", context)
        body_html = self.render_template("estimation_confirmation.html", context)
        
        return self.send_email(email, subject, body_text, body_html)
    
    def send_admin_notification(
        self,
        notification_type: str,
        data: Dict[str, Any]
    ) -> bool:
        """
        Envoie une notification à l'administrateur.
        
        Args:
            notification_type: Type de notification (newsletter, estimation)
            data: Données de la notification
            
        Returns:
            bool: True si l'email a été envoyé avec succès
        """
        admin_email = os.getenv("ADMIN_EMAIL", "j.dussauld@orange.fr")
        
        if notification_type == "newsletter":
            title = "Nouvel abonnement newsletter"
        elif notification_type == "estimation":
            title = "Nouvelle demande d'estimation"
        else:
            return False
        
        subject = f"🔔 {title}"
        
        context = {
            "title": title,
            "notification_type": notification_type,
            "data": data,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        
        body_text = self.render_template("admin_notification.txt", context)
        body_html = self.render_template("admin_notification.html", context)
        
        return self.send_email(admin_email, subject, body_text, body_html)


# Instance globale du service
email_service = EmailService()
