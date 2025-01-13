import { resourcesLinks } from "../constants";

const Footer = () => {
  return (
    <footer className="mt-20 border-t py-10 border-neutral-700">
      <div className="flex flex-col lg:flex-row justify-between items-center px-4 sm:px-8">
        {/* Left Section */}
        <div className="text-left mb-1 lg:mb-0">
          <h1 className="text-2xl font-bold text-orange-500">GetScheme</h1>
          <p className="mt-4 text-black-400">
            Unlock opportunities tailored for you.
          </p>
        </div>

        {/* Right Section */}
        <div className="w-full lg:w-auto">
          <h3 className="text-md font-semibold mb-1 text-orange-500">Resources</h3>
          <ul className="space-y-2">
            {resourcesLinks.map((link, index) => (
              <li key={index}>
                <a
                  href={link.href}
                  className="text-black-300 hover:text-white"
                >
                  {link.text}
                </a>
              </li>
            ))}
          </ul>
        </div>
      </div>
      {/* Footer Credit */}
      <div className="text-center mt-8 text-orange-500">
        Made by Team Ayush
      </div>
    </footer>
  );
};

export default Footer;
