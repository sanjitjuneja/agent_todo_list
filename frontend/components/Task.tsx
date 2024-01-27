import React from "react";
import { taskType } from "./types/Ttask";
import { Input } from "@/components/ui/input";
import { HiPlay } from "react-icons/hi2";
import { RxCross2 } from "react-icons/rx";
import Modal from "@/components/ui/Modal";

type taskProps = {
  index: number;
  task: taskType;
  editTasks: (i: number, value: string) => void;
  deleteTask: (t: taskType) => Promise<void>;
  playTask: (i: number) => void;
};

function Task({ task, editTasks, deleteTask, index, playTask }: taskProps) {
  return (
    <div
      className={`border-gray-200 rounded-md cursor-pointer border py-1 ${
        task.completed && "border-green-200"
      }`}
      key={index}
    >
      <div className="flex flex-row items-center">
        <div
          className=" opacity-40 hover:opacity-95 px-4"
          onClick={() => playTask(index)}
        >
          <HiPlay className="w-4 h-4 text-blue-600" />
        </div>
        <Input
          className="border-none focus:border-none"
          value={task.input}
          onChange={(e) => editTasks(index, e.target.value)}
        />
        <div
          className=" opacity-40 hover:opacity-95 px-4"
          onClick={() => deleteTask(task)}
        >
          <RxCross2 className="w-4 h-4 text-gray-9 00" />
        </div>
      </div>
    </div>
  );
}

export default Task;
