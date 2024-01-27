"use client";

import React, { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { HiPlay } from "react-icons/hi2";
import { RxCross2 } from "react-icons/rx";
import Modal from "@/components/ui/Modal";

type task = {
  name: string;
  completed: Boolean;
  result: string;
};

export default function Home() {
  const [tasks, setTasks] = useState<task[]>([
    { name: "task 1", completed: false, result: "" },
    { name: "task 2", completed: false, result: "" },
    { name: "task 3", completed: false, result: "" },
    { name: "task 4", completed: false, result: "" },
    { name: "task 5", completed: false, result: "" },
  ]);

  const editTasks = (index: number, text: string) => {
    const newTasks = tasks.map((task, i) => {
      if (i === index) {
        return { ...task, name: text };
      }
      return task;
    });
    setTasks(newTasks);
  };

  const addTask = () => {
    const newTasks = [...tasks];
    newTasks.push({ name: "", completed: false, result: "" });
    setTasks(newTasks);
  };

  const deleteTask = (index: number) => {
    const newTasks = tasks.filter((task, i) => {
      return i !== index;
    });
    setTasks(newTasks);
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
                    value={task.name}
                    onChange={(e) => editTasks(index, e.target.value)}
                  />
                  <div
                    className=" opacity-40 hover:opacity-95 px-4"
                    onClick={() => deleteTask(index)}
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
