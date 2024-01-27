"use client";
import React from "react";
import { Button } from "./ui/button";
import { useRouter } from "next/navigation";
const navItemStyles = "text-large font-semibold";

function Navbar() {
  const router = useRouter();
  return (
    <div className="border-b border-gray-100 flex flex-row px-20 space-x-8 py-2 items-center">
      <div className="font-bold">Name</div>
      <div
        className="font-normal p-2 hover:text-gray-800 cursor-pointer text-gray-600"
        onClick={() => router.push("/")}
      >
        Home
      </div>
      <div
        className="font-normal p-2 hover:text-gray-800 cursor-pointer text-gray-600"
        onClick={() => router.push("/agents")}
      >
        Agents
      </div>
    </div>
  );
}

export default Navbar;
