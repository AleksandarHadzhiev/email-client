'use client'

import { useEffect, useState } from "react";

export default function Index() {

    console.log("MEOW")
    const [userData, setUserData] = useState()
    const BASE_URL = "http://127.0.0.1:8000/google/callback"

    const fetchData = async () => {
        try {
            const res = await fetch(BASE_URL, { method: "POST", body: JSON.stringify({ pathname: window.location.href }) });
            const data = await res.json();
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