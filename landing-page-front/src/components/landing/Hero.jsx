import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { ArrowRight, Sparkles, Code2, Smartphone, Mail, AlertCircle } from "lucide-react";
// eslint-disable-next-line no-unused-vars
import { motion } from "framer-motion";
import { subscribeNewsletter } from "@/services/api";

export default function Hero({ onGetQuote }) {
  const [showNewsletter, setShowNewsletter] = useState(false);
  const [email, setEmail] = useState("");
  const [subscribed, setSubscribed] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  const handleNewsletterSubmit = async (e) => {
    e.preventDefault();
    if (email) {
      setIsSubmitting(true);
      setError("");

      try {
        await subscribeNewsletter(email);
        setSubscribed(true);
        setEmail("");
        setTimeout(() => {
          setSubscribed(false);
          setShowNewsletter(false);
        }, 2000);
      } catch (err) {
        setError("Une erreur est survenue. Veuillez réessayer.");
        console.error("Newsletter subscription error:", err);
      } finally {
        setIsSubmitting(false);
      }
    }
  };
  return (
    <div className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-indigo-950 via-purple-900 to-indigo-950">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div
          animate={{
            scale: [1, 1.2, 1],
            rotate: [0, 90, 0],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: "linear",
          }}
          className="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-br from-blue-600/20 to-purple-600/20 rounded-full blur-3xl"
        />
        <motion.div
          animate={{
            scale: [1.2, 1, 1.2],
            rotate: [90, 0, 90],
          }}
          transition={{
            duration: 25,
            repeat: Infinity,
            ease: "linear",
          }}
          className="absolute -bottom-1/2 -right-1/2 w-full h-full bg-gradient-to-tl from-purple-600/20 to-blue-600/20 rounded-full blur-3xl"
        />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-6 py-20 text-center">
        <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }}>
          <h1 className="text-6xl md:text-8xl font-bold text-white mb-6 tracking-tight">
            Transformez vos
            <span className="block bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">idées en réalité</span>
          </h1>

          <p className="text-xl md:text-2xl text-slate-300 mb-12 max-w-3xl mx-auto leading-relaxed">
            Développement d'applications et sites web sur mesure. De la conception à la mise en ligne, nous créons des solutions digitales qui font la différence.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Button
              size="lg"
              onClick={onGetQuote}
              className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-8 py-6 text-base rounded-full shadow-2xl shadow-purple-500/50 transition-all duration-300 hover:scale-105 font-semibold"
            >
              Obtenir une estimation gratuite
              <ArrowRight className="ml-2 w-5 h-5" />
            </Button>
            <Button
              size="lg"
              variant="outline"
              onClick={() => setShowNewsletter(true)}
              className="bg-white/10 backdrop-blur-md border-2 border-white/30 text-white hover:bg-white/20 px-8 py-6 text-base rounded-full transition-all duration-300 font-semibold"
            >
              S'abonner à la newsletter
              <Mail className="ml-2 w-5 h-5" />
            </Button>
          </div>
        </motion.div>

        {/* Newsletter Dialog */}
        <Dialog open={showNewsletter} onOpenChange={setShowNewsletter}>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle className="text-2xl font-bold bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent">Restez informé</DialogTitle>
              <DialogDescription className="text-slate-600">Inscrivez-vous à notre newsletter pour recevoir nos dernières actualités et offres exclusives.</DialogDescription>
            </DialogHeader>
            {subscribed ? (
              <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="text-center py-8">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Mail className="w-8 h-8 text-green-600" />
                </div>
                <h3 className="text-xl font-semibold text-slate-900 mb-2">Merci de votre inscription !</h3>
                <p className="text-slate-600">Vous recevrez bientôt nos actualités.</p>
              </motion.div>
            ) : (
              <form onSubmit={handleNewsletterSubmit} className="space-y-4 pt-4">
                <div className="space-y-2">
                  <Input type="email" placeholder="votre@email.com" value={email} onChange={(e) => setEmail(e.target.value)} required className="text-base" />
                  {error && (
                    <div className="flex items-center gap-2 text-red-600 text-sm">
                      <AlertCircle className="w-4 h-4" />
                      <span>{error}</span>
                    </div>
                  )}
                </div>
                <Button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-semibold disabled:opacity-50"
                  size="lg"
                >
                  {isSubmitting ? "Inscription..." : "S'abonner"}
                  <ArrowRight className="ml-2 w-5 h-5" />
                </Button>
              </form>
            )}
          </DialogContent>
        </Dialog>

        {/* Services icons */}
        <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8, delay: 0.3 }} className="grid grid-cols-2 md:grid-cols-3 gap-6 mt-20 max-w-4xl mx-auto">
          {[
            { icon: Code2, label: "Sites Web", color: "from-blue-400 to-cyan-400" },
            { icon: Smartphone, label: "Applications", color: "from-purple-400 to-pink-400" },
            { icon: Sparkles, label: "Solutions IA", color: "from-yellow-400 to-orange-400" },
          ].map((item, idx) => (
            <motion.div key={idx} whileHover={{ scale: 1.05, y: -5 }} className="bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-6 transition-all duration-300">
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${item.color} flex items-center justify-center mb-4 mx-auto`}>
                <item.icon className="w-6 h-6 text-white" />
              </div>
              <p className="text-white font-medium">{item.label}</p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </div>
  );
}
