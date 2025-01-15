'use client'

import { useEffect, useState } from "react";
import { useSearchParams } from 'next/navigation'

export default function Index() {

    console.log("MEOW")
    const searchParams = useSearchParams()
    const [userData, setUserData] = useState()
    const GOOGLE_URL = "http://127.0.0.1:8000/google/callback"
    const MICROSOFT_URL = "http://127.0.0.1:8000/microsoft/response"

    const fetchData = async () => {
        const state = searchParams.get("state")
        if (state === null) {
            googleSSO()
        }
        else {
            microsoftSSO()
        }
    }


    const googleSSO = async () => {
        try {
            const res = await fetch(GOOGLE_URL, { method: "POST", body: JSON.stringify({ pathname: window.location.href }) });
            const data = await res.json();
            setUserData(data)
        } catch (err) {
            throw err;
        }
    }


    const microsoftSSO = async () => {
        try {
            const res = await fetch(MICROSOFT_URL, { method: "POST", body: JSON.stringify({ pathname: window.location.href }) });
            const data = await res.json();
            console.log(data)
            setUserData(data)
        } catch (err) {
            throw err;
        }
    }
    useEffect(() => {
        fetchData()

    }, [])
    return (
        <div>
            <button>Meow</button>
        </div>
    )
}