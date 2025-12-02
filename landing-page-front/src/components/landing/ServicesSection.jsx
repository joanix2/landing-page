import React from "react";
// eslint-disable-next-line no-unused-vars
import { motion } from "framer-motion";
import { Globe, Smartphone, ShoppingCart, Zap, Palette, Shield } from "lucide-react";

const services = [
  {
    icon: Globe,
    title: "Sites Vitrine",
    description: "Sites web élégants et performants pour présenter votre entreprise",
    gradient: "from-blue-500 to-blue-600",
    bgColor: "bg-blue-500",
  },
  {
    icon: ShoppingCart,
    title: "E-commerce",
    description: "Boutiques en ligne complètes avec paiement sécurisé et gestion de stock",
    gradient: "from-pink-500 to-pink-600",
    bgColor: "bg-pink-500",
  },
  {
    icon: Smartphone,
    title: "Applications Mobiles",
    description: "Apps iOS et Android natives ou cross-platform",
    gradient: "from-green-500 to-green-600",
    bgColor: "bg-green-500",
  },
  {
    icon: Zap,
    title: "Applications Web",
    description: "Plateformes web complexes et outils métier sur mesure",
    gradient: "from-orange-500 to-red-600",
    bgColor: "bg-orange-500",
  },
  {
    icon: Palette,
    title: "Design UI/UX",
    description: "Interfaces modernes et expériences utilisateur optimales",
    gradient: "from-pink-400 to-pink-600",
    bgColor: "bg-pink-400",
  },
  {
    icon: Shield,
    title: "Maintenance & Support",
    description: "Accompagnement continu et évolutions de votre solution",
    gradient: "from-purple-500 to-indigo-600",
    bgColor: "bg-purple-500",
  },
];

export default function ServicesSection() {
  return (
    <section className="py-24 bg-gray-50">
      <div className="max-w-7xl mx-auto px-6">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.6 }} className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4">Nos Services</h2>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">Des solutions complètes pour tous vos besoins digitaux</p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {services.map((service, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: idx * 0.1 }}
              whileHover={{ y: -8, transition: { duration: 0.3 } }}
              className="group relative bg-white rounded-2xl p-8 shadow-md hover:shadow-xl transition-all duration-300"
            >
              <div className={`w-16 h-16 rounded-2xl ${service.bgColor} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                <service.icon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">{service.title}</h3>
              <p className="text-slate-600 leading-relaxed">{service.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
