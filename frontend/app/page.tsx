"use client";

import React, { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { HiPlay } from "react-icons/hi2";
import { RxCross2 } from "react-icons/rx";
import Modal from "@/components/ui/Modal";
import { Amplify } from 'aws-amplify';
import config from '../src/aws-exports.js';
import { generateClient } from "aws-amplify/api";
import { createTask } from '../src/graphql/mutations';
import { listTasks } from '../src/graphql/queries';
import { deleteTask } from '../src/graphql/mutations';

const client = generateClient()

Amplify.configure(config);

type task = {
  id: string;
  input: string;
  output: string;
  completed: Boolean;
};

export default function Home() {

  const fetchTasks = async () => {
    // List all items
    const result = await client.graphql({
      query: listTasks
    }) as { data: { listTasks: { items: task[] } } };
    const fetchedTasks: task[] = result.data?.listTasks.items || [];
    setTasks(fetchedTasks);
  }

  useEffect(() => {
    fetchTasks();
  }, []);

  const [tasks, setTasks] = useState<task[]>([]);

  const editTasks = (index: number, text: string) => {
    const newTasks = tasks.map((task, i) => {
      if (i === index) {
        return { ...task, input: text };
      }
      return task;
    });
    setTasks(newTasks);
  };


  const addTask = async () => {
    const newTask = await client.graphql({
      query: createTask,
      variables: {
        input: {
          input: "Enter your task here",
          output: "",
          completed: false
        }
      }
    });
    fetchTasks();
  };

  const removeTask = async (task: task) => {
    const deletedTask = await client.graphql({
      query: deleteTask,
      variables: {
          input: {
              id: task.id
          }
      }
    });
    fetchTasks();
  };

  return (
    <div>
      <div className="text-xl text-gray-800 font-semibold mb-4">Your Tasks</div>
      <div className="flex flex-col space-y-4">
        {tasks &&
          tasks.map((task, index) => {
            return (
              <div
                className={`border-gray-200 rounded-md cursor-pointer border py-1 ${
                  task.completed && "bg-green-200"
                }`}
                key={index}
              >
                <div className="flex flex-row items-center">
                  <div className=" opacity-40 hover:opacity-95 px-4">
                    <HiPlay className="w-4 h-4 text-green-600" />
                  </div>
                  <Input
                    className="border-none focus:border-none"
                    type="email"
                    value={task.input}
                    onChange={(e) => editTasks(index, e.target.value)}
                  />
                  <div
                    className=" opacity-40 hover:opacity-95 px-4"
                    onClick={() => removeTask(task)}
                  >
                    <RxCross2 className="w-4 h-4 text-gray-9 00" />
                  </div>
                </div>
              </div>
            );
          })}
        <div
          className="border-gray-200 rounded-md cursor-pointer flex flex-row items-center justify-center hover:bg-gray-50"
          onClick={addTask}
        >
          <div className="p-4 text-gray-600">+</div>
          <div className="text-sm text-gray-600">Add Task</div>
        </div>
      </div>
    </div>
  );
}
