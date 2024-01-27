import React, { ReactNode } from "react";
type modalProps = {
  close: () => void;
  visible: boolean;
  children: ReactNode;
};

function Modal({ close, visible, children }: modalProps) {
  return (
    <div
      className={`absolute w-screen h-screen backdrop-blur-sm bg-black/20 left-0 top-0 items-center justify-center flex ${
        visible
          ? "opacity-100 pointer-events-auto"
          : "opacity-0 pointer-events-none"
      } transition-all duration-300`}
    >
      <div className="md:w-2/3 h-3/4 w-11/12">
        <div
          className="bg-white p-6 rounded-md space-y-4 flex flex-col"
          onClick={(e) => e.stopPropagation()}
        >
          {children}
        </div>
      </div>
    </div>
  );
}

export default Modal;
