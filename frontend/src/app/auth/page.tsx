'use client'

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import LoadingScreen from "@/components/loadingScreen";
import ExternalServiceHandler from "../../APICalls/ExternalServiceRouterHandler";
export default function Index() {
    const externalExerivceHandler = ExternalServiceHandler.instance
    const router = useRouter()
    const [username, setUsername] = useState("")

    const fetchData = async () => {
        const url = window.location.href
        const request_body = { pathname: url }
        try {
            const response = await externalExerivceHandler.auth(request_body, new URL("http://127.0.0.1:8000/auth"));
            if (response) {
                setUsername(response.email)
                localStorage.setItem("jwt", response.token)
                localStorage.setItem("username", response.email)
                setTimeout(() => {
                    redirect(response.email)
                }, 1500);
            }
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
            {/* <div className="animated-block"> </div> */}
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