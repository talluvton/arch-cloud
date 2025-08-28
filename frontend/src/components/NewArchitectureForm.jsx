import { useState } from "react";
import api from "../api";

function isValidHttpUrl(string) {
    let url;
    try {
        url = new URL(string);
    } catch (_) {
        return false;
    }
    return url.protocol === "http:" || url.protocol === "https:";
}

const NewArchitectureForm = ({ setArchitectures, setShowForm }) => {
  const [architectureUrl, setArchitectureUrl] = useState("")
  const [isUploading, setIsUploading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

    async function handleSubmit(e) {
        e.preventDefault();
        if (!isValidHttpUrl(architectureUrl)) {
            setErrorMsg("Please enter a valid URL (http/https).");
            return;
        }

        setIsUploading(true);
        try {
            const res = await api.post("/scrape", { url: architectureUrl});
            const items = Array.isArray(res.data) ? res.data : [res.data];
            setArchitectures(prev => [...items, ...prev]);
            setArchitectureUrl("");
            setShowForm(false);
        } catch (error) {
            const msg = error?.response?.data?.detail || "Failed to scrape URL.";
            setErrorMsg(msg);
        } finally {
            setIsUploading(false);
        }
    }


  return (
    <form className="add-architecture-form" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Url"
        value={architectureUrl}
        onChange={(e) => setArchitectureUrl(e.target.value)}
        disabled={isUploading}
      />
      {errorMsg && (
        <p className="message" aria-live="polite" style={{ color: "#ffb4b4", fontSize: "0.85rem", marginTop: 6 }}>
            {errorMsg}
        </p>
      )}

      <button className="btn btn-large" disabled={isUploading}>
        {isUploading ? "Scraping..." : "Scrape"}
      </button>
    </form>
  );
};

export default NewArchitectureForm;