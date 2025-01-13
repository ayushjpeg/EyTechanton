import { BotMessageSquare } from "lucide-react";
import { BatteryCharging } from "lucide-react";
import { Fingerprint } from "lucide-react";
import { ShieldHalf } from "lucide-react";
import { PlugZap } from "lucide-react";
import { GlobeLock } from "lucide-react";
import user1 from "../assets/profile-pictures/user1.jpg";
import user2 from "../assets/profile-pictures/user2.jpg";
import user3 from "../assets/profile-pictures/user3.jpg";
import user4 from "../assets/profile-pictures/user4.jpg";
import user5 from "../assets/profile-pictures/user5.jpg";
import user6 from "../assets/profile-pictures/user6.jpg";

export const navItems = [
  {label: "Home", href: "/"},
  { label: "Features", href: "/features" },  // updated to include path
  { label: "Steps", href: "/workflow" },
  { label: "Pricing", href: "/pricing" },
  { label: "Testimonials", href: "/testimonials" },
];

export const testimonials = [
  {
    user: "Priya Sharma",
    location: "Madhya Pradesh",
    image: user1,
    text: "This platform made it so much easier for me to access government schemes. The AI-guided application process saved me countless hours!",
  },
  {
    user: "Ramesh Verma",
    location: "Uttar Pradesh",
    image: user2,
    text: "I used to struggle with finding the right schemes for my family. This tool recommended the perfect options for us in minutes!",
  },
  {
    user: "Sita Devi",
    location: "Bihar",
    image: user3,
    text: "I can now stay updated on new schemes without needing to travel or stand in long queues. It's a game-changer for rural citizens.",
  },
];


export const features = [
  {
    icon: <BotMessageSquare />,
    text: "AI-Powered Scheme Discovery",
    description: "Use our AI to match you with the most relevant government schemes based on your profile and needs.",
  },
  {
    icon: <Fingerprint />,
    text: "Document Verification",
    description: "Seamless document upload and AI-based verification to eliminate the hassle of manual checks.",
  },
  {
    icon: <ShieldHalf />,
    text: "Eligibility Checker",
    description: "Get instant insights into your eligibility for various schemes without any manual calculations.",
  },
  {
    icon: <BatteryCharging />,
    text: "Real-Time Updates",
    description: "Stay informed with real-time updates on your application status and new schemes.",
  },
  {
    icon: <PlugZap />,
    text: "Guided Application Process",
    description: "Step-by-step guidance for filling out and submitting applications, reducing errors and delays.",
  },
  {
    icon: <GlobeLock />,
    text: "Secure Data Handling",
    description: "Your personal information and documents are encrypted and stored securely.",
  },
];


export const checklistItems = [
  {
    title: "Upload Documents",
    description: "Upload essential documents such as Aadhaar, income certificates, and more.",
  },
  {
    title: "Check Eligibility",
    description: "Our AI checks your eligibility for various government schemes.",
  },
  {
    title: "Discover Schemes",
    description: "View a curated list of schemes tailored to your needs.",
  },
  {
    title: "Apply with Ease",
    description: "Fill out applications in a guided and error-free process.",
  },
];


export const pricingOptions = [
  {
    title: "Basic",
    price: "Free",
    features: [
      "Access to AI based scheme discovery",
      "Document upload and verification",
      "Basic eligibility check and scheme details",
    ],
  },
  {
    title: "Pro",
    price: "₹99",
    features: [
      "Advanced scheme recommendations",
      "Priority application assistance",
      "Real-time updates and notifications",
    ],
  },
  {
    title: "Enterprise",
    price: "₹499",
    features: [
      "Dedicated support for organizations",
      "Bulk document processing",
      "Insights and analytics for scheme participation",
    ],
  },
];

export const resourcesLinks = [
  { href: "/", text: "Home" },
  { href: "/features", text: "Features" },
  { href: "/workflow", text: "Steps" },
  { href: "/pricing", text: "Pricing" },
  { href: "/testimonials", text: "Testimonials" },
];

export const platformLinks = [
  { href: "#", text: "Features" },
  { href: "#", text: "Supported Devices" },
  { href: "#", text: "System Requirements" },
  { href: "#", text: "Downloads" },
  { href: "#", text: "Release Notes" },
];

export const communityLinks = [
  { href: "#", text: "Events" },
  { href: "#", text: "Meetups" },
  { href: "#", text: "Conferences" },
  { href: "#", text: "Hackathons" },
  { href: "#", text: "Jobs" },
];
