import React, { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Progress } from "@/components/ui/progress";
import { FileText, Sparkles, User, CheckCircle, Loader2 } from "lucide-react";
import { getAISuggestions, createEstimation } from "@/services/api";
// eslint-disable-next-line no-unused-vars
import { motion, AnimatePresence } from "framer-motion";

export default function QuoteWizard({ isOpen, onClose }) {
  const [step, setStep] = useState(1);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const [quoteData, setQuoteData] = useState({
    project_description: "",
    project_type: "",
    number_of_pages: "",
    features: [],
    design_level: "",
    timeline: "",
    budget_range: "",
    has_content: false,
    needs_maintenance: false,
    full_name: "",
    email: "",
    phone: "",
    company: "",
  });

  const progress = (step / 3) * 100;

  const analyzeDescription = async () => {
    setIsProcessing(true);
    try {
      console.log("📤 Envoi de la description à l'API...");
      const result = await getAISuggestions(quoteData.project_description);

      // Debug: afficher la réponse complète de l'API
      console.log("📥 API Response COMPLETE:", JSON.stringify(result, null, 2));

      // Les données sont dans result.suggestions
      const suggestions = result.suggestions || {};

      console.log("📋 Suggestions extraites:");
      console.log("  - type_projet:", suggestions.type_projet);
      console.log("  - nombre_pages:", suggestions.nombre_pages);
      console.log("  - delai_souhaite:", suggestions.delai_souhaite);
      console.log("  - budget:", suggestions.budget);
      console.log("  - liste_pages:", suggestions.liste_pages);

      // Mapper les résultats de l'API vers notre structure de données
      // Convertir le type de projet en valeur du select
      let projectType = "";
      if (suggestions.type_projet) {
        const typeMap = {
          "Site Vitrine": "site_vitrine",
          "Site E-commerce": "site_ecommerce",
          "Application Web": "application_web",
          "Application Mobile": "application_mobile",
          "E-commerce": "site_ecommerce",
          Vitrine: "site_vitrine",
        };
        projectType = typeMap[suggestions.type_projet] || "custom";
      }

      // Utiliser directement les valeurs du backend (pas de conversion)
      const mappedData = {
        ...quoteData,
        project_type: projectType,
        number_of_pages: suggestions.nombre_pages ? String(suggestions.nombre_pages) : "",
        features: Array.isArray(suggestions.liste_pages) ? suggestions.liste_pages : [],
        timeline: suggestions.delai_souhaite || "",
        budget_range: suggestions.budget || "",
      };

      console.log("✅ Mapped data:", JSON.stringify(mappedData, null, 2));
      console.log("🔄 Mise à jour de quoteData...");
      setQuoteData(mappedData);

      // Petit délai pour s'assurer que le state est bien mis à jour avant de changer d'étape
      setTimeout(() => {
        console.log("➡️ Passage à l'étape 2");
        setStep(2);
      }, 100);
    } catch (error) {
      console.error("❌ Error analyzing description:", error);
      alert("Une erreur est survenue lors de l'analyse. Veuillez continuer manuellement.");
      setStep(2);
    } finally {
      setIsProcessing(false);
    }
  };
  const handleSubmit = async () => {
    setIsProcessing(true);
    try {
      // Convertir uniquement le type de projet
      const typeProjectMap = {
        site_vitrine: "Site Vitrine",
        site_ecommerce: "Site E-commerce",
        application_web: "Application Web",
        application_mobile: "Application Mobile",
        custom: "Projet Sur Mesure",
      };

      // Mapper les données vers le format de l'API
      const estimationData = {
        client: {
          email: quoteData.email,
          nom: quoteData.full_name,
          telephone: quoteData.phone,
          entreprise: quoteData.company,
        },
        estimation: {
          description_projet: quoteData.project_description,
          type_projet: typeProjectMap[quoteData.project_type] || quoteData.project_type,
          nombre_pages: parseInt(quoteData.number_of_pages) || 0,
          delai_souhaite: quoteData.timeline,
          budget: quoteData.budget_range,
        },
      };

      await createEstimation(estimationData);

      setIsSuccess(true);
      setTimeout(() => {
        onClose();
        setIsSuccess(false);
        setStep(1);
        setQuoteData({
          project_description: "",
          project_type: "",
          number_of_pages: "",
          features: [],
          design_level: "",
          timeline: "",
          budget_range: "",
          has_content: false,
          needs_maintenance: false,
          full_name: "",
          email: "",
          phone: "",
          company: "",
        });
      }, 3000);
    } catch (error) {
      console.error("Error submitting quote:", error);
      alert("Une erreur est survenue lors de l'envoi de votre demande. Veuillez réessayer.");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-3xl font-bold text-slate-900">Obtenir une estimation gratuite</DialogTitle>
          <Progress value={progress} className="mt-4" />
          <div className="flex items-center justify-between mt-2">
            <p className="text-sm text-slate-600">Étape {step} sur 3</p>
            {step === 1 && (
              <Button onClick={() => setStep(2)} variant="outline" size="sm" className="text-sm">
                Suivant
              </Button>
            )}
          </div>
        </DialogHeader>

        <AnimatePresence mode="wait">
          {!isSuccess ? (
            <motion.div key={step} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="pt-6">
              {/* Étape 1: Description libre */}
              {step === 1 && (
                <div className="space-y-6">
                  <div className="flex items-start gap-4 p-4 bg-blue-50 rounded-xl">
                    <Sparkles className="w-6 h-6 text-blue-600 mt-1 flex-shrink-0" />
                    <p className="text-slate-700">Décrivez votre projet en quelques lignes. Notre IA analysera vos besoins pour pré-remplir le formulaire détaillé.</p>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="description">Décrivez votre projet *</Label>
                    <Textarea
                      id="description"
                      value={quoteData.project_description}
                      onChange={(e) => setQuoteData((prev) => ({ ...prev, project_description: e.target.value }))}
                      placeholder="Exemple : Je souhaite créer un site e-commerce pour vendre des produits artisanaux. J'ai besoin d'environ 20 pages, d'un système de paiement sécurisé, et d'un design moderne et élégant. Mon budget est d'environ 10 000€..."
                      className="min-h-48"
                      required
                    />
                  </div>

                  <Button
                    onClick={analyzeDescription}
                    disabled={!quoteData.project_description || isProcessing}
                    className="w-full h-14 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white text-lg rounded-xl"
                  >
                    {isProcessing ? (
                      <>
                        <Loader2 className="mr-2 w-5 h-5 animate-spin" />
                        Analyse en cours...
                      </>
                    ) : (
                      <>
                        <Sparkles className="mr-2 w-5 h-5" />
                        Analyser avec l'IA
                      </>
                    )}
                  </Button>
                </div>
              )}

              {/* Étape 2: Formulaire détaillé */}
              {step === 2 && (
                <div className="space-y-6">
                  {console.log("🎨 Rendu Étape 2 - quoteData:", quoteData)}
                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <Label htmlFor="project_type">Type de projet *</Label>
                      <Select value={quoteData.project_type} onValueChange={(val) => setQuoteData((prev) => ({ ...prev, project_type: val }))}>
                        <SelectTrigger className="h-12">
                          <SelectValue placeholder="Sélectionner" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="site_vitrine">Site Vitrine</SelectItem>
                          <SelectItem value="site_ecommerce">Site E-commerce</SelectItem>
                          <SelectItem value="application_web">Application Web</SelectItem>
                          <SelectItem value="application_mobile">Application Mobile</SelectItem>
                          <SelectItem value="custom">Projet Sur Mesure</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="number_of_pages">Nombre de pages/écrans *</Label>
                      <Input
                        id="number_of_pages"
                        type="number"
                        value={quoteData.number_of_pages}
                        onChange={(e) => setQuoteData((prev) => ({ ...prev, number_of_pages: e.target.value }))}
                        placeholder="5"
                        className="h-12"
                      />
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <Label htmlFor="timeline">Délai souhaité *</Label>
                      <Select value={quoteData.timeline} onValueChange={(val) => setQuoteData((prev) => ({ ...prev, timeline: val }))}>
                        <SelectTrigger className="h-12">
                          <SelectValue placeholder="Sélectionner" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="Rapide">Rapide</SelectItem>
                          <SelectItem value="Normal">Normal</SelectItem>
                          <SelectItem value="Flexible">Flexible</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="budget_range">Budget approximatif</Label>
                    <Select value={quoteData.budget_range} onValueChange={(val) => setQuoteData((prev) => ({ ...prev, budget_range: val }))}>
                      <SelectTrigger className="h-12">
                        <SelectValue placeholder="Sélectionner" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Moins de 5 000€">Moins de 5 000€</SelectItem>
                        <SelectItem value="5 000€ - 10 000€">5 000€ - 10 000€</SelectItem>
                        <SelectItem value="10 000€ - 20 000€">10 000€ - 20 000€</SelectItem>
                        <SelectItem value="Plus de 20 000€">Plus de 20 000€</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="flex gap-4">
                    <Button variant="outline" onClick={() => setStep(1)} className="flex-1 h-12">
                      Retour
                    </Button>
                    <Button onClick={() => setStep(3)} className="flex-1 h-12 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700">
                      Continuer
                    </Button>
                  </div>
                </div>
              )}

              {/* Étape 3: Coordonnées */}
              {step === 3 && (
                <div className="space-y-6">
                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <Label htmlFor="full_name">Nom complet *</Label>
                      <Input
                        id="full_name"
                        value={quoteData.full_name}
                        onChange={(e) => setQuoteData((prev) => ({ ...prev, full_name: e.target.value }))}
                        placeholder="Jean Dupont"
                        className="h-12"
                        required
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="company">Entreprise</Label>
                      <Input id="company" value={quoteData.company} onChange={(e) => setQuoteData((prev) => ({ ...prev, company: e.target.value }))} placeholder="Votre entreprise" className="h-12" />
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <Label htmlFor="email">Email *</Label>
                      <Input
                        id="email"
                        type="email"
                        value={quoteData.email}
                        onChange={(e) => setQuoteData((prev) => ({ ...prev, email: e.target.value }))}
                        placeholder="jean@entreprise.fr"
                        className="h-12"
                        required
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="phone">Téléphone</Label>
                      <Input
                        id="phone"
                        type="tel"
                        value={quoteData.phone}
                        onChange={(e) => setQuoteData((prev) => ({ ...prev, phone: e.target.value }))}
                        placeholder="+33 6 12 34 56 78"
                        className="h-12"
                      />
                    </div>
                  </div>

                  <div className="flex gap-4">
                    <Button variant="outline" onClick={() => setStep(2)} className="flex-1 h-12">
                      Retour
                    </Button>
                    <Button
                      onClick={handleSubmit}
                      disabled={!quoteData.full_name || !quoteData.email || isProcessing}
                      className="flex-1 h-12 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700"
                    >
                      {isProcessing ? (
                        <>
                          <Loader2 className="mr-2 w-5 h-5 animate-spin" />
                          Envoi...
                        </>
                      ) : (
                        <>
                          <FileText className="mr-2 w-5 h-5" />
                          Recevoir mon estimation
                        </>
                      )}
                    </Button>
                  </div>
                </div>
              )}
            </motion.div>
          ) : (
            <motion.div key="success" initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} className="py-12 text-center">
              <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: "spring", delay: 0.2 }}>
                <CheckCircle className="w-24 h-24 text-green-500 mx-auto mb-6" />
              </motion.div>
              <h3 className="text-3xl font-bold text-slate-900 mb-4">Estimation envoyée !</h3>
              <p className="text-xl text-slate-600">Consultez votre email pour voir l'estimation détaillée.</p>
            </motion.div>
          )}
        </AnimatePresence>
      </DialogContent>
    </Dialog>
  );
}
