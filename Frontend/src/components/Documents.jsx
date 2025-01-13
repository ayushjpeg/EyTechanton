import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Documents = () => {
  const navigate = useNavigate();
  const [files, setFiles] = useState([]);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const selectedFiles = Array.from(event.target.files);

    // Validate file types
    const validFiles = selectedFiles.filter((file) => {
      const fileType = file.type;
      return (
        fileType === "application/pdf" ||
        fileType.startsWith("image/png") ||
        fileType.startsWith("image/jpeg")
      );
    });

    if (validFiles.length !== selectedFiles.length) {
      setError(
        "Some files were rejected. Only PNG, JPG, JPEG, or PDF files are allowed."
      );
    } else {
      setError(""); // Clear previous errors
    }

    // Update state with valid files
    setFiles((prevFiles) => [...prevFiles, ...validFiles]);
  };

  const handleUpload = async () => {
    if (files.length === 0) {
      alert("Please select files to upload.");
      return;
    }
  
    const formData = new FormData();
    files.forEach((file) => {
      formData.append("files", file);
    });
  
    try {
      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });
  
      if (response.ok) {
        const data = await response.json();
        alert("Upload successful!");
        console.log("Response data:", data);
        
        // Navigate to Details page and pass data
        navigate("/details", { state: { formData: data } });
      } else {
        const errorData = await response.json();
        setError(errorData.error || "Upload failed.");
      }
    } catch (error) {
      console.error("Error during upload:", error);
      setError("An error occurred during file upload.");
    }
  };
  

  return (
    <div className="min-h-screen flex flex-col items-center bg-black-100 py-10 px-4">
      <h1 className="text-2xl font-bold text-orange-700 mb-6">
        Upload Your Documents
      </h1>
      <div className="bg-gray rounded-lg shadow-md p-6 w-full max-w-3xl">
        <input
          type="file"
          accept=".png, .jpg, .jpeg, .pdf"
          multiple
          onChange={handleFileChange}
          className="border border-gray-300 rounded-md w-full p-2 mb-4"
        />
        <button
          onClick={handleUpload}
          className="bg-gradient-to-r from-orange-500 to-orange-800 text-white py-2 px-6 rounded-md hover:opacity-90"
        >
          Upload Files
        </button>
        {error && <p className="text-red-500 mt-2">{error}</p>}
        {files.length > 0 && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold mb-2">Selected Files:</h2>
            <ul className="list-disc pl-5">
              {files.map((file, index) => (
                <li key={index} className="text-white-700">
                  {file.name} ({(file.size / 1024).toFixed(2)} KB)
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default Documents;
