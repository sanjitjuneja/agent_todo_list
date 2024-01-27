"use client";

import React, { useEffect, useState } from "react";
import { taskType } from "@/components/types/Ttask";
import Task from "@/components/Task";
import Modal from "@/components/ui/Modal";
import { Amplify } from "aws-amplify";
import config from "../src/aws-exports.js";
import { generateClient } from "aws-amplify/api";
import { listTasks } from "../src/graphql/queries";
import { deleteTask, updateTask, createTask } from "../src/graphql/mutations";

import AgentPage from "@/components/ModalPages/AgentPage";
import ClarificationPage from "@/components/ModalPages/ClarificationPage";
import ResultsPage from "@/components/ModalPages/ResultsPage";

const client = generateClient();

Amplify.configure(config);

export default function Home() {
  const fetchTasks = async () => {
    // List all items
    const result = (await client.graphql({
      query: listTasks,
    })) as { data: { listTasks: { items: taskType[] } } };
    const fetchedTasks: taskType[] = result.data?.listTasks.items || [];
    setTasks(fetchedTasks);
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const [tasks, setTasks] = useState<taskType[]>([]);

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
          completed: false,
        },
      },
    });
    fetchTasks();
  };

  const removeTask = async (task: taskType) => {
    const deletedTask = await client.graphql({
      query: deleteTask,
      variables: {
        input: {
          id: task.id,
        },
      },
    });
    fetchTasks();
  };

  const [showModal, setShowModal] = useState(false);
  const closeModal = () => setShowModal(false);
  const openModal = () => setShowModal(true);

  const [loading, setLoading] = useState(false);
  const [modalPage, setModalPage] = useState<number>(1);
  const [selectedTask, setSelectedTask] = useState<taskType>();
  const [agent, setAgent] = useState({}); // TODO: create agent type

  const [clarifyingQuestion, setClarifiyingQuestion] = useState("");
  const [clarificationResponse, setClarificationResponse] =
    useState<string>("");

  const editClarification = (input: string) => {
    setClarificationResponse(input);
  };

  const [result, setResult] = useState("");

  const playTask = async (index: number) => {
    for (let i = 0; i < tasks.length; i++) {
      if (i === index) {
        const updatedTask = await client.graphql({
          query: updateTask,
          variables: {
            input: {
              id: tasks[i].id,
              input: tasks[i].input,
              output: tasks[i].output,
              completed: tasks[i].completed,
            },
          },
        });
      }
    }
    setSelectedTask(tasks[index]);
    setClarificationResponse("");
    setResult("");
    setModalPage(1);
    //setLoading(true);
    //make api call to classification
    openModal();
  };

  const nextPage = () => {
    //hardcode which modalPage to navigate to and which apis to call
    setLoading(true);
    if (modalPage === 1) {
      // call generate
      setModalPage(2);
    }
    if (modalPage === 2) {
      //call get results
      setModalPage(3);
    }
  };

  return (
    <div>
      <Modal close={closeModal} visible={showModal}>
        {modalPage === 1 && (
          <AgentPage
            loading={loading}
            selectedAgent={agent}
            input={selectedTask?.input || ""}
            next={nextPage}
          />
        )}
        {modalPage === 2 && (
          <ClarificationPage
            questions={clarifyingQuestion}
            loading={loading}
            setResponse={editClarification}
            value={clarificationResponse}
            next={nextPage}
          />
        )}
        {modalPage === 3 && (
          <ResultsPage results={result} loading={loading} close={closeModal} />
        )}
      </Modal>

      <div className="text-xl text-gray-800 font-semibold mb-4">Your Tasks</div>
      <div className="flex flex-col space-y-4">
        {tasks &&
          tasks.map((task, index) => {
            return (
              <Task
                task={task}
                index={index}
                editTasks={editTasks}
                deleteTask={removeTask}
                playTask={playTask}
              />
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
