'use client'

import { useEffect, useState } from "react";
import { useSearchParams } from 'next/navigation'
import { printTreeView } from "next/dist/build/utils";

export default function Index() {

    console.log("MEOW")
    const searchParams = useSearchParams()
    const [usename, setUsername] = useState("")
    const AUTH_URL = "http://127.0.0.1:8000/auth"

    const fetchData = async () => {
        try {
            const res = await fetch(AUTH_URL, { method: "POST", body: JSON.stringify({ pathname: window.location.href }) });
            const data = await res.json();
            console.log(data)
            setUsername(data)
        } catch (err) {
            throw err;
        }
    }

    useEffect(() => {
        fetchData()

    }, [])
    return (
        <div>
            <button>You have logged in successfully. Welcome to the email client {usename}.</button>
        </div>
    )
}