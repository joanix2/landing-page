// Base44 API Client Mock
// Replace with actual API integration

export const base44 = {
  entities: {
    Quote: {
      create: async (data) => {
        console.log("Creating quote:", data);
        // Mock API call
        return new Promise((resolve) => {
          setTimeout(() => {
            resolve({ id: Date.now(), ...data });
          }, 1000);
        });
      },
    },
    Appointment: {
      create: async (data) => {
        console.log("Creating appointment:", data);
        // Mock API call
        return new Promise((resolve) => {
          setTimeout(() => {
            resolve({ id: Date.now(), ...data });
          }, 1000);
        });
      },
    },
  },
  integrations: {
    Core: {
      SendEmail: async ({ to, subject, html }) => {
        console.log("Sending email:", { to, subject, html });
        // Mock email sending
        return new Promise((resolve) => {
          setTimeout(() => {
            resolve({ success: true });
          }, 500);
        });
      },
    },
  },
};
