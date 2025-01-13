import { useRef } from "react";
import img1 from "../assets/img1.png";
import img2 from "../assets/img2.png";
import img3 from "../assets/img3.png";

const HeroSection = () => {
  const scrollContainerRef = useRef(null);

  const scrollLeft = () => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollLeft -= 200;
    }
  };

  const scrollRight = () => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollLeft += 200;
    }
  };

  // Array of images
  const images = [img1, img2, img3];

  return (
    <div className="flex flex-col items-center mt-6 lg:mt-0 px-6 sm:px-4 md:px-8">
      <h1 className="text-3xl sm:text-4xl lg:text-5xl text-center tracking-wide font-semibold">
        Discover Government Schemes
        <span className="bg-gradient-to-r from-orange-500 to-red-800 text-transparent bg-clip-text">
          {" "}
          Tailored for You
        </span>
      </h1>
      <div className="flex items-center mt-6 w-full justify-center">
        <button onClick={scrollLeft} className="mx-2 text-orange-500">
          ◀
        </button>
        <div
          className="flex overflow-x-auto w-full justify-start gap-4"
          ref={scrollContainerRef}
          style={{
            scrollBehavior: "smooth",
            padding: "20px",
          }}
        >
          {/* Spacer Div for Padding */}
          <div style={{ width: "10px", flexShrink: 0 }}></div>

          {/* Image Frames */}
          {[...Array(6)].map((_, index) => (
            <div className="flex-shrink-0" key={index}>
              <img
                src={images[index % images.length]} // Use modulo to loop through images
                alt={`Illustration ${index + 1}`}
                className="rounded-lg border border-orange-700 shadow-sm shadow-orange-400"
                style={{
                  width: "100%", // makes image responsive
                  maxWidth: "500px", // max width for large screens
                  height: "auto", // keeps the aspect ratio intact
                }}
              />
            </div>
          ))}
        </div>
        <button onClick={scrollRight} className="mx-2 text-orange-500">
          ▶
        </button>
      </div>
      <p className="mt-10 text-lg text-center text-neutral-500 max-w-4xl px-4 sm:px-2">
        Simplify your access to government schemes with our AI-driven platform. 
        Upload your documents or provide your details to instantly discover the benefits 
        you're eligible for. Save time, avoid queues, and get the support you need effortlessly!
      </p>
      <div className="flex justify-center my-10 gap-4">
        <a
          href="/Documents"
          className="bg-gradient-to-r from-orange-500 to-orange-800 py-3 px-6 sm:px-4 rounded-md"
        >
          Upload Documents
        </a>
        <a
          href="/Details"
          className="py-3 px-6 sm:px-4 rounded-md border text-center"
        >
          Enter Details Manually
        </a>
      </div>
    </div>
  );
};

export default HeroSection;
