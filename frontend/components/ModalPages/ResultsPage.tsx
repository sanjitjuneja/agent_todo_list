import React, {useEffect} from "react";
import Loading from "../Loading";
import { Button } from "../ui/button";
type resultsPageProps = {
  loading: boolean;
  close: () => void;
  results: string;
};

function ResultsPage({ loading, close, results }: resultsPageProps) {
  if (loading) {
    return <Loading />;
  }
  const getExecution = async () => {
    const response = await fetch('/api/clarification');
    const result = await response.text();
    console.log(result);
    // setAgents(response.data);
  }

  useEffect(() => {
    getExecution();
  }, []);


  return (
    <div>
      {results}
      <div className="flex flex-row space-x-2">
        <Button onClick={close}>Submit</Button>
      </div>
    </div>
  );
}

export default ResultsPage;
