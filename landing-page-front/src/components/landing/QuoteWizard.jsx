import React from "react";
// eslint-disable-next-line no-unused-vars
import { motion } from "framer-motion";
import { Globe, Smartphone, ShoppingCart, Zap, Palette, Shield } from "lucide-react";

const services = [
  {
    icon: Globe,
    title: "Sites Vitrine",
    description: "Sites web élégants et performants pour présenter votre entreprise",
    gradient: "from-blue-500 to-cyan-500",
  },
  {
    icon: ShoppingCart,
    title: "E-commerce",
    description: "Boutiques en ligne complètes avec paiement sécurisé et gestion de stock",
    gradient: "from-purple-500 to-pink-500",
  },
  {
    icon: Smartphone,
    title: "Applications Mobiles",
    description: "Apps iOS et Android natives ou cross-platform",
    gradient: "from-green-500 to-emerald-500",
  },
  {
    icon: Zap,
    title: "Applications Web",
    description: "Plateformes web complexes et outils métier sur mesure",
    gradient: "from-orange-500 to-red-500",
  },
  {
    icon: Palette,
    title: "Design UI/UX",
    description: "Interfaces modernes et expériences utilisateur optimales",
    gradient: "from-pink-500 to-rose-500",
  },
  {
    icon: Shield,
    title: "Maintenance & Support",
    description: "Accompagnement continu et évolutions de votre solution",
    gradient: "from-indigo-500 to-blue-500",
  },
];

export default function Services() {
  return (
    <section className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-6">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.6 }} className="text-center mb-16">
          <h2 className="text-5xl md:text-6xl font-bold text-slate-900 mb-6">Nos Services</h2>
          <p className="text-xl text-slate-600 max-w-3xl mx-auto">Des solutions complètes pour tous vos besoins digitaux</p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((service, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: idx * 0.1 }}
              whileHover={{ y: -8, transition: { duration: 0.3 } }}
              className="group relative bg-white rounded-3xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-slate-100"
            >
              <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${service.gradient} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                <service.icon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-slate-900 mb-4">{service.title}</h3>
              <p className="text-slate-600 leading-relaxed">{service.description}</p>
              <div
                className={`absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r ${service.gradient} transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300 rounded-b-3xl`}
              />
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
