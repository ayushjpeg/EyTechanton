import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import HeroSection from "./components/HeroSection";
import FeatureSection from "./components/FeatureSection";
import Workflow from "./components/Workflow";
import Footer from "./components/Footer";
import Pricing from "./components/Pricing";
import Testimonials from "./components/Testimonials";
import Details from "./components/Details";
import Documents from "./components/Documents";
import Result from "./components/Result";

const App = () => {
  const mockSchemeData = [
    {
      "Scheme Name":
        "Dr. Ambedakar Centrally Sponsored Scheme of Post-Matric Scholarships for the Economically Backward Class (EBC) Students",
      "Scheme URL": "https://www.myscheme.gov.in/schemes/dacsspostmsebcs",
      Tags: ["EBC", "Economically Backward Class", "Post Matric", "Scholarship", "Student"],
      "Eligibility Criteria to Verify": [
        "The scholarships will be open to Indian nationals belonging to the General Category (Other than Schedule Caste, Schedule Tribe and Other Backward Classes).",
        "These scholarships will be given for the study of all recognized post-matriculation or post-secondary courses pursued in Government institutions.",
        "Employed students whose income combined with the income of their parents/guardians does not exceed ₹ 1,00,000 per annum shall be eligible for post-matric scholarships to the extent of reimbursement of all compulsorily payable non-refundable fees.",
        "In the case of unemployed students whose parents/guardians income from all sources does not exceed ₹ 1,00,000 per annum will be entitled to the scholarship under the Scheme."
      ]
    },
    {
      "Scheme Name": "The West Bengal Incentive Scheme: Additional Incentive on Generation of Employment",
      "Scheme URL": "https://www.myscheme.gov.in/schemes/wbisaige",
      Tags: ["Employment Generation", "Entrepreneurship", "Incentives", "Reimbursement", "Subsidy", "Tourism", "Tourism Units", "Waiver"],
      "Eligibility Criteria to Verify": []
    }
  ];

  return (
    <Router>
      <Navbar />
      <div className="max-w-7xl mx-auto pt-20 px-6">
        {/* Set up the Routes for different pages */}
        <Routes>
          {/* Home page - All sections */}
          <Route
            path="/"
            element={
              <>
                <HeroSection />
                <FeatureSection />
                <Workflow />
                <Pricing />
                <Testimonials />
              </>
            }
          />

          {/* Individual pages */}
          <Route path="/features" element={<FeatureSection />} />
          <Route path="/workflow" element={<Workflow />} />
          <Route path="/pricing" element={<Pricing />} />
          <Route path="/testimonials" element={<Testimonials />} />
          <Route path="/details" element={<Details />} />
          <Route path="/documents" element={<Documents />} />
          <Route
            path="/result"
            element={<Result  />}
          />
        </Routes>
      </div>
      <Footer />
    </Router>
  );
};

export default App;
