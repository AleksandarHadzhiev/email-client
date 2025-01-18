'use client'

import { useEffect } from "react";
import Navbar from "@/components/navigation";
import Sidebar from "@/components/sidebar";
import Login from "@/components/login";
import MailBody from "@/components/MailBody";
export default function Home() {

  const BASE_URL = "http://localhost:8000"
  let username
  // Get the value from local storage if it exists
  username = localStorage.getItem("username") || ""


  useEffect(() => {
    const fetchData = async () => {
      await fetch(BASE_URL).then(async (res) => {
        console.log(await res.json())
      }).catch((err) => {
        console.log(err)
      })
    }

    fetchData()
  })

  return (
    <>
      {
        username === "" ? (<Login />) : (<div className="grid grid-rows-10 h-screen w-full" >
          <Navbar />
          <main className="row-span-9 grid grid-cols-10">
            <Sidebar />
            <MailBody />
          </main>
        </div>)
      }
    </>
  );
}
