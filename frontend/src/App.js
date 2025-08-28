import React, { useState, useEffect } from "react";
import api from "./api";
import "./App.css";
import Header from "./components/Header";
import ArchitecturesList from "./components/ArchitecturesList";
import NewArchitectureForm from "./components/NewArchitectureForm";
import Loader from "./components/Loader";

const App = () => {
  const [showForm, setShowForm] = useState(false);
  const [architectures, setArchitectures] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(function () {
    async function getArchitectures() {
      setIsLoading(true);
      try {
        const response = await api.get("/architectures/");
        setArchitectures(response.data);
      } catch (error) {
        alert("There was a problem getting data");
      } finally {
        setIsLoading(false);
      }
    }
    getArchitectures();
  }, []);

  return (
    <>
      <Header showForm={showForm} setShowForm={setShowForm} />

      {showForm ? (
        <NewArchitectureForm setArchitectures={setArchitectures} setShowForm={setShowForm} />
      ) : null}

      <main className="main">
        {isLoading ? (
          <Loader />
        ) : (
          <ArchitecturesList architectures={architectures} />
        )}
      </main>
    </>
  );
};

export default App;