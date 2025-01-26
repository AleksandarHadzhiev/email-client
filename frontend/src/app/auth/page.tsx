'use client'

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import LoadingScreen from "@/components/loadingScreen";
export default function Index() {

    const router = useRouter()
    const [username, setUsername] = useState("")
    const AUTH_URL = "http://127.0.0.1:8000/auth"

    const fetchData = async () => {
        try {
            const res = await fetch(AUTH_URL, { method: "POST", body: JSON.stringify({ pathname: window.location.href }) });
            const data = await res.json();
            setUsername(data)
            localStorage.setItem("username", data)
            setTimeout(() => {
                redirect(data)
            }, 1500);
        } catch (err) {
            throw err;
        }
    }

    const redirect = (data: String) => {
        const isLoggedIn = data.includes("@")
        if (isLoggedIn)
            router.push("/")
    }

    useEffect(() => {
        fetchData()
    }, [])
    return (
        <div className="w-full h-screen flex justify-center items-center align-center">
            {
                username !== "" ? (
                    <h1>You have logged in successfully. Welcome to the email client <strong>{username}</strong>.</h1>
                ) : (
                    <LoadingScreen />
                )
            }

        </div >
    )
}