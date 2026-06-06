import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Match from "./pages/Match";
import Results from "./pages/Results";

export default function App() {
  return (
    <BrowserRouter>
      <Toaster position="top-right" toastOptions={{ duration: 3000 }} />
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/match" element={<Match />} />
          <Route path="/results" element={<Results />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
