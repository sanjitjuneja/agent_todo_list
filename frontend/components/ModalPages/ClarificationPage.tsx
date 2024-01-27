import React, {useEffect} from "react";
import Loading from "../Loading";
import { Button } from "../ui/button";
import { Textarea } from "../ui/textarea";

type clarificationPageProps = {
  questions: string;
  loading: boolean;
  setResponse: (s: string) => void;
  next: () => void;
  value: string;
};

function ClarificationPage({
  loading,
  questions,
  setResponse,
  next,
  value,
}: clarificationPageProps) {
  if (loading) {
    return <Loading />;
  }

  const getClarification = async () => {
    const response = await fetch('/api/clarification');
    const result = await response.text();
    console.log(result);
    // setAgents(response.data);
  }

  useEffect(() => {
    getClarification();
  }, []);

  return (
    <div className="flex flex-col space-y-4">
      <div className="font-semibold text-gray-700">Clarifying Questions</div>
      <div>{questions}</div>
      <Textarea
        onChange={(e) => setResponse(e.target.value)}
        value={value}
      ></Textarea>
      <div className="flex flex-row space-x-2">
        <Button onClick={next}>Submit</Button>
      </div>
    </div>
  );
}

export default ClarificationPage;
