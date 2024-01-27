"use client";

import { Amplify } from 'aws-amplify';
import config from '../src/aws-exports.js';
import { Button } from "../components/ui/button";
import { generateClient } from "aws-amplify/api";
import { createTask } from './graphql/mutations';

const client = generateClient()

Amplify.configure(config);

export default function Home() {

  

  return (
  <>hi</>
    <Button onClick={}>

    </Button>
    
  )
  
}
