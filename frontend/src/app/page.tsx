'use client'

import { useEffect, useState } from "react";
import Navbar from "@/components/navigation";
import Sidebar from "@/components/Emails/sidebar";
import Login from "@/components/Login";
import MailBody from "@/components/Emails/MailBody";
import ExternalServiceHandler from "./ExternalServiceRouterHandler";
export default function Home() {
  let username = ""
  // Get the value from local storage if it exists
  const externalServiceHandler = ExternalServiceHandler.instance
  const getToken = async () => {
    await externalServiceHandler.getToken(new URL("http://localhost:8000"))
  }
  useEffect(() => {
    getToken()
  }, [])
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
