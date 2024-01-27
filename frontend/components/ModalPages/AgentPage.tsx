import React from "react";
import Loading from "../Loading";
import { Button } from "../ui/button";
type agentSelectProps = {
  input: string;
  loading: boolean;
  selectedAgent: {};
  next: () => void;
};
function AgentSelect({
  input,
  loading,
  selectedAgent,
  next,
}: agentSelectProps) {
  if (loading) {
    return <Loading />;
  }
  return (
    <div className="flex flex-col space-y-4">
      <div className="font-semibold text-gray-700">
        Task: <span className="font-medium">{input}</span>
      </div>
      <div className="font-semibold text-gray-700">Selected Agent:</div>
      <div>{"selectedAgent"}</div>
      <div className="flex flex-row space-x-2">
        <Button>Regenerate</Button>
        <Button onClick={next}>Next</Button>
      </div>
    </div>
  );
}

export default AgentSelect;
