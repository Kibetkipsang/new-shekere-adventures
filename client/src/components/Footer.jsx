import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="bg-black text-white py-4 text-center h-40">
      <p className="mt-20">&copy; {new Date().getFullYear()} Shekere Adventures. All rights reserved.</p>
    </footer>
  );
}