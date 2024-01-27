"use client";
import React from "react";
import { useState, useEffect } from "react";
import Loading from "@/components/Loading";
import axios from "axios";
//call backend to get agents

function page() {

  const getAgents = async () => {
    const response = await fetch('/api/agents');
    const result = await response.text();
    console.log(result);
    // setAgents(response.data);
  }

  useEffect(() => {
    getAgents();
  }, []);
  
  const [agents, setAgents] = useState(["Awesome Agent", "Average Agent"]); //make agents type
  return (
    <div>
      <div className="text-xl text-gray-800 font-semibold mb-4">Agents</div>
      <div className="flex flex-col space-y-2">
        {agents &&
          agents.map((agent, i) => {
            return (
              <div className="p-2 border border-gray-100 rounded-lg flex flex-row">
                <div className="w-10 h-10 bg-blue-600 text-white rounded-full flex flex-row items-center justify-center mr-4">
                  {agent.at(0)}
                </div>
                <div>
                  <div className="font-semibold text-gray-800">{agent}</div>
                  <div className="text-gray-700">Agent Description</div>
                </div>
              </div>
            );
          })}
      </div>
    </div>
  );
}

export default page;

/*
 {name, description, actions: {}, png}
*/
