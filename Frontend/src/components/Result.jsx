import React from "react";
import { useLocation } from "react-router-dom";

const extractKeywords = (text) => {
  const stopWords = ["the", "and", "of", "to", "in", "for", "with", "on"];
  return text
    .split(" ")
    .filter((word) => word.length > 3 && !stopWords.includes(word.toLowerCase()))
    .slice(0, 2);
};

const Result = () => {
  const location = useLocation();
  const { result } = location.state.data || {}; // Safeguard against missing state
  //console.log("Result data:", result);

  let schemes = [];

  if (result && Array.isArray(result)) {
    // Check if result is a valid array and parse it
    schemes = result.map((item) => {
      try {
        // Clean out the surrounding ```json and parse it
        const cleanedItem = item.replace(/```json|```/g, "");
        const parsedItem = JSON.parse(cleanedItem);
        
        return parsedItem;
      } catch (error) {
        console.error("Error parsing item", error);
        return null;
      }
    }).filter(Boolean); // Remove any null values from parsing errors
  }
  //console.log("Parsed schemes:", schemes);
  schemes = schemes[0];
  console.log(schemes);

  return (
    <div className="container mx-auto mt-10 px-4">
      <h1 className="text-3xl sm:text-4xl font-bold text-center mb-10">
        Scheme Details
      </h1>
      <div className="space-y-6">
        {schemes.map((scheme, index) => (
          <div
            key={index}
            className="border border-neutral-700 rounded-md p-6 shadow-lg bg-white flex flex-col sm:flex-row gap-6"
          >
            {/* Scheme Name and Link */}
            <div className="flex-1">
              <h2 className="text-xl font-semibold mb-2 text-black">
                {scheme["Scheme Name"]}
              </h2>
              <a
                href={scheme["Scheme URL"]}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500 hover:text-blue-700 text-sm break-all"
              >
                Visit Scheme
              </a>
            </div>

            {/* Tags */}
            <div className="flex-1">
              <h3 className="font-medium text-black mb-2">Tags:</h3>
              <div className="flex flex-wrap gap-2">
                {scheme.Tags.map((tag, tagIndex) => (
                  <span
                    key={tagIndex}
                    className="px-3 py-1 bg-gray-200 rounded-full text-sm text-neutral-800"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>

            {/* Eligibility Criteria */}
            {scheme["Eligibility Criteria to Verify"].length > 0 && (
              <div className="flex-1">
                <h3 className="font-medium text-black mb-2">Eligibility:</h3>
                <div className="flex flex-wrap gap-2">
                  {scheme["Eligibility Criteria to Verify"].map(
                    (criteria, criteriaIndex) => {
                      const keywords = extractKeywords(criteria);
                      return (
                        <span
                          key={criteriaIndex}
                          className="relative px-3 py-1 bg-gray-200 rounded-full text-sm text-neutral-800 group cursor-pointer"
                        >
                          {keywords}
                          {/* Tooltip for full eligibility details */}
                          <div className="absolute left-0 top-full mt-2 w-64 p-2 bg-white border border-neutral-700 shadow-lg rounded-md text-neutral-600 text-sm opacity-0 group-hover:opacity-100 transition-opacity z-10">
                            {criteria}
                          </div>
                        </span>
                      );
                    }
                  )}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Result;
