// Configuration de l'API
// En production, utilise l'URL relative /api qui sera gérée par le proxy
// En développement local (hors Docker), utilise localhost:8000
const API_URL = import.meta.env.VITE_API_URL || "/api";

// Debug : afficher l'URL utilisée
console.log("🔗 API_URL:", API_URL, "- Environment:", import.meta.env.MODE);

/**
 * Service pour l'abonnement à la newsletter
 * @param {string} email - L'email à abonner
 * @returns {Promise<Object>} - Réponse de l'API
 */
export const subscribeNewsletter = async (email) => {
  try {
    const response = await fetch(`${API_URL}/newsletter`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error subscribing to newsletter:", error);
    throw error;
  }
};

/**
 * Service pour créer une estimation
 * @param {Object} data - Les données de l'estimation
 * @param {Object} data.client - Informations du client
 * @param {string} data.client.email - Email du client
 * @param {string} [data.client.nom] - Nom du client
 * @param {string} [data.client.telephone] - Téléphone du client
 * @param {string} [data.client.entreprise] - Entreprise du client
 * @param {Object} data.estimation - Détails de l'estimation
 * @param {string} data.estimation.description_projet - Description du projet
 * @param {string} data.estimation.type_projet - Type de projet
 * @param {number} data.estimation.nombre_pages - Nombre de pages
 * @param {string} data.estimation.delai_souhaite - Délai souhaité
 * @param {string} data.estimation.budget - Budget estimé
 * @returns {Promise<Object>} - Réponse de l'API
 */
export const createEstimation = async (data) => {
  try {
    const response = await fetch(`${API_URL}/estimations`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error creating estimation:", error);
    throw error;
  }
};

/**
 * Service pour obtenir des suggestions IA
 * @param {string} description_projet - Description du projet
 * @returns {Promise<Object>} - Suggestions de l'IA
 */
export const getAISuggestions = async (description_projet) => {
  try {
    const response = await fetch(`${API_URL}/ai/suggest`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ description_projet }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error getting AI suggestions:", error);
    throw error;
  }
};
