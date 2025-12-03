import { useState, useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Loader2, CheckCircle2, XCircle, Mail, ArrowLeft } from "lucide-react";

const API_BASE_URL = import.meta.env.VITE_API_URL || "/api";

export default function Unsubscribe() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const email = searchParams.get("email");

  const [loading, setLoading] = useState(false);
  const [clientData, setClientData] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [alreadyUnsubscribed, setAlreadyUnsubscribed] = useState(false);

  // Vérifier si l'email existe au chargement
  useEffect(() => {
    const checkClientStatus = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${API_BASE_URL}/newsletter/client/${encodeURIComponent(email)}`);

        if (response.ok) {
          const data = await response.json();
          setClientData(data);
          setAlreadyUnsubscribed(!data.newsletter);
        } else if (response.status === 404) {
          setError("Cet email n'est pas inscrit à notre newsletter.");
        } else {
          setError("Erreur lors de la vérification de votre email.");
        }
      } catch {
        setError("Impossible de se connecter au serveur.");
      } finally {
        setLoading(false);
      }
    };

    if (email) {
      checkClientStatus();
    }
  }, [email]);

  const handleUnsubscribe = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(`${API_BASE_URL}/newsletter/unsubscribe/${encodeURIComponent(email)}`, {
        method: "POST",
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(true);
      } else {
        setError(data.detail || "Erreur lors de la désinscription.");
      }
    } catch {
      setError("Impossible de se connecter au serveur.");
    } finally {
      setLoading(false);
    }
  };

  if (!email) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex items-center justify-center p-4">
        <Card className="max-w-md w-full">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <XCircle className="h-5 w-5 text-red-500" />
              Email manquant
            </CardTitle>
            <CardDescription>Aucun email n'a été fourni dans l'URL.</CardDescription>
          </CardHeader>
          <CardFooter>
            <Button onClick={() => navigate("/")} variant="outline" className="w-full">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Retour à l'accueil
            </Button>
          </CardFooter>
        </Card>
      </div>
    );
  }

  if (loading && !clientData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex items-center justify-center p-4">
        <Card className="max-w-md w-full">
          <CardContent className="pt-6">
            <div className="flex flex-col items-center gap-4">
              <Loader2 className="h-8 w-8 animate-spin text-purple-600" />
              <p className="text-gray-600">Vérification en cours...</p>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (success) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex items-center justify-center p-4">
        <Card className="max-w-md w-full">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-green-600">
              <CheckCircle2 className="h-5 w-5" />
              Désinscription réussie
            </CardTitle>
            <CardDescription>Vous avez été désinscrit avec succès</CardDescription>
          </CardHeader>
          <CardContent>
            <Alert className="bg-green-50 border-green-200">
              <CheckCircle2 className="h-4 w-4 text-green-600" />
              <AlertDescription className="text-green-800">
                L'email <strong>{email}</strong> ne recevra plus nos newsletters.
              </AlertDescription>
            </Alert>
            <p className="mt-4 text-sm text-gray-600">Nous sommes désolés de vous voir partir. Si vous changez d'avis, vous pourrez toujours vous réinscrire depuis notre site web.</p>
          </CardContent>
          <CardFooter className="flex gap-2">
            <Button onClick={() => navigate("/")} variant="default" className="flex-1">
              Retour à l'accueil
            </Button>
          </CardFooter>
        </Card>
      </div>
    );
  }

  if (alreadyUnsubscribed) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex items-center justify-center p-4">
        <Card className="max-w-md w-full">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Mail className="h-5 w-5 text-gray-500" />
              Déjà désinscrit
            </CardTitle>
            <CardDescription>Vous êtes déjà désinscrit de notre newsletter</CardDescription>
          </CardHeader>
          <CardContent>
            <Alert>
              <Mail className="h-4 w-4" />
              <AlertDescription>
                L'email <strong>{email}</strong> ne reçoit déjà plus nos newsletters.
              </AlertDescription>
            </Alert>
          </CardContent>
          <CardFooter>
            <Button onClick={() => navigate("/")} variant="outline" className="w-full">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Retour à l'accueil
            </Button>
          </CardFooter>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex items-center justify-center p-4">
      <Card className="max-w-md w-full">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Mail className="h-5 w-5 text-purple-600" />
            Se désinscrire de la newsletter
          </CardTitle>
          <CardDescription>Confirmez votre désinscription</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {error && (
            <Alert variant="destructive">
              <XCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600 mb-2">Email concerné :</p>
            <p className="font-medium text-gray-900">{email}</p>
          </div>

          <div className="text-sm text-gray-600 space-y-2">
            <p>Vous êtes sur le point de vous désinscrire de notre newsletter. Vous ne recevrez plus :</p>
            <ul className="list-disc list-inside space-y-1 ml-2">
              <li>Nos dernières actualités</li>
              <li>Nos conseils et astuces web</li>
              <li>Nos offres exclusives</li>
            </ul>
          </div>

          <Alert>
            <AlertDescription className="text-sm">💡 Vous pourrez toujours vous réinscrire ultérieurement depuis notre site web.</AlertDescription>
          </Alert>
        </CardContent>
        <CardFooter className="flex gap-2">
          <Button onClick={() => navigate("/")} variant="outline" className="flex-1" disabled={loading}>
            <ArrowLeft className="mr-2 h-4 w-4" />
            Annuler
          </Button>
          <Button onClick={handleUnsubscribe} variant="destructive" className="flex-1" disabled={loading}>
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Désinscription...
              </>
            ) : (
              "Me désinscrire"
            )}
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}
