'use client'

import { useState } from "react";
import Navbar from "@/components/Navigation";
import Sidebar from "@/components/Sidebar";
import Login from "@/components/Login";
import MailBody from "@/components/MailBody";
export default function Home() {
  let username
  // Get the value from local storage if it exists
  username = localStorage.getItem("username") || ""
  const [mail, setMail] = useState(null)
  return (
    <>
      {
        username === "" ? (<Login />) : (<div className="grid grid-rows-10 h-screen w-full" >
          <Navbar />
          <main className="row-span-9 grid grid-cols-10">
            <Sidebar setMail={setMail} />
            <MailBody email={mail} />
          </main>
        </div>)
      }
    </>
  );
}
