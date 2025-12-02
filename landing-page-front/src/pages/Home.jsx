import React, { useState } from "react";
import Hero from "../components/landing/Hero";
import ServicesSection from "../components/landing/ServicesSection";
import QuoteWizardDialog from "../components/landing/Services";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowRight, Mail, Phone, MapPin } from "lucide-react";
// eslint-disable-next-line no-unused-vars
import { motion } from "framer-motion";
import { subscribeNewsletter } from "@/services/api";

export default function Home() {
  const [showQuote, setShowQuote] = useState(false);
  const [showNewsletter, setShowNewsletter] = useState(false);
  const [email, setEmail] = useState("");
  const [emailCTA, setEmailCTA] = useState("");
  const [subscribed, setSubscribed] = useState(false);
  const [subscribedCTA, setSubscribedCTA] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmittingCTA, setIsSubmittingCTA] = useState(false);

  const handleNewsletterSubmit = async (e) => {
    e.preventDefault();
    if (email) {
      setIsSubmitting(true);
      try {
        await subscribeNewsletter(email);
        setSubscribed(true);
        setEmail("");
        setTimeout(() => setSubscribed(false), 3000);
      } catch (error) {
        console.error("Newsletter subscription error:", error);
        alert("Une erreur est survenue. Veuillez réessayer.");
      } finally {
        setIsSubmitting(false);
      }
    }
  };

  const handleNewsletterCTASubmit = async (e) => {
    e.preventDefault();
    if (emailCTA) {
      setIsSubmittingCTA(true);
      try {
        await subscribeNewsletter(emailCTA);
        setSubscribedCTA(true);
        setEmailCTA("");
        setTimeout(() => {
          setSubscribedCTA(false);
          setShowNewsletter(false);
        }, 2000);
      } catch (error) {
        console.error("Newsletter subscription error:", error);
        alert("Une erreur est survenue. Veuillez réessayer.");
      } finally {
        setIsSubmittingCTA(false);
      }
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <Hero onGetQuote={() => setShowQuote(true)} />

      <ServicesSection />

      {/* CTA Section */}
      <section className="py-24 bg-gradient-to-br from-indigo-950 via-purple-900 to-indigo-950 relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0zNiAxOGMzLjMxNCAwIDYgMi42ODYgNiA2cy0yLjY4NiA2LTYgNi02LTIuNjg2LTYtNiAyLjY4Ni02IDYtNiIgc3Ryb2tlPSJyZ2JhKDI1NSwyNTUsMjU1LDAuMSkiLz48L2c+PC9zdmc+')] opacity-20" />

        <div className="max-w-5xl mx-auto px-6 text-center relative z-10">
          <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.8 }}>
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">Prêt à démarrer votre projet ?</h2>
            <p className="text-lg text-slate-300 mb-12 max-w-2xl mx-auto">Obtenez une estimation personnalisée ou restez informé de nos actualités</p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Button size="lg" onClick={() => setShowQuote(true)} className="bg-white text-slate-900 hover:bg-slate-100 px-8 py-6 text-lg rounded-full shadow-xl font-semibold">
                Obtenir une estimation gratuite
                <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
              <Button
                size="lg"
                variant="outline"
                onClick={() => setShowNewsletter(true)}
                className="border-2 border-white/30 bg-white/5 text-white hover:bg-white/10 px-8 py-6 text-lg rounded-full backdrop-blur-sm font-semibold"
              >
                S'abonner à la newsletter
                <Mail className="ml-2 w-5 h-5" />
              </Button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Newsletter Dialog for CTA Section */}
      {showNewsletter && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 px-4" onClick={() => setShowNewsletter(false)}>
          <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="bg-white rounded-2xl p-8 max-w-md w-full shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-2xl font-bold bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent mb-2">Restez informé</h3>
            <p className="text-slate-600 mb-6">Inscrivez-vous à notre newsletter pour recevoir nos dernières actualités et offres exclusives.</p>

            {subscribedCTA ? (
              <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="text-center py-8">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Mail className="w-8 h-8 text-green-600" />
                </div>
                <h4 className="text-xl font-semibold text-slate-900 mb-2">Merci de votre inscription !</h4>
                <p className="text-slate-600">Vous recevrez bientôt nos actualités.</p>
              </motion.div>
            ) : (
              <form onSubmit={handleNewsletterCTASubmit} className="space-y-4">
                <Input type="email" placeholder="votre@email.com" value={emailCTA} onChange={(e) => setEmailCTA(e.target.value)} required className="text-base" />
                <Button
                  type="submit"
                  disabled={isSubmittingCTA}
                  className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-semibold disabled:opacity-50"
                  size="lg"
                >
                  {isSubmittingCTA ? "Inscription..." : "S'abonner"}
                  <ArrowRight className="ml-2 w-5 h-5" />
                </Button>
              </form>
            )}
          </motion.div>
        </div>
      )}

      {/* Footer */}
      <footer className="bg-slate-950 text-white py-16">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid md:grid-cols-3 gap-12 mb-8">
            <div>
              <h3 className="text-2xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">Axynis</h3>
              <p className="text-slate-400 text-sm">Création d'applications et sites web sur mesure</p>
            </div>
            <div>
              <h4 className="font-semibold mb-4 text-white">Contact</h4>
              <div className="space-y-3 text-slate-400 text-sm">
                <div className="flex items-start gap-3">
                  <Mail className="w-4 h-4 mt-0.5 flex-shrink-0" />
                  <span>contact@studio.fr</span>
                </div>
                <div className="flex items-start gap-3">
                  <Phone className="w-4 h-4 mt-0.5 flex-shrink-0" />
                  <span>+33 1 23 45 67 89</span>
                </div>
                <div className="flex items-start gap-3">
                  <MapPin className="w-4 h-4 mt-0.5 flex-shrink-0" />
                  <span>Paris, France</span>
                </div>
              </div>
            </div>
            <div>
              <h4 className="font-semibold mb-4 text-white">Newsletter</h4>
              <p className="text-slate-400 text-sm mb-4">Restez informé de nos dernières actualités</p>
              <form onSubmit={handleNewsletterSubmit} className="flex flex-col gap-2">
                <Input
                  type="email"
                  placeholder="Votre email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="bg-slate-900 border-slate-700 text-white placeholder:text-slate-500"
                />
                <Button type="submit" disabled={isSubmitting} className="bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white disabled:opacity-50">
                  {subscribed ? "Inscrit !" : isSubmitting ? "Inscription..." : "S'abonner"}
                </Button>
              </form>
            </div>
          </div>
          <div className="border-t border-slate-800 pt-8 text-center text-slate-500 text-sm">
            <p>&copy; 2025 Axynis. Tous droits réservés.</p>
          </div>
        </div>
      </footer>

      <QuoteWizardDialog isOpen={showQuote} onClose={() => setShowQuote(false)} />
    </div>
  );
}
