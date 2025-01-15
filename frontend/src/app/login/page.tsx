'use client'

import { useRouter } from "next/navigation";

export default function Index() {

    const router = useRouter()
    const GOOGLE_SSO = "http://127.0.0.1:8000/google/login"
    const MICROSOFT_SSO = "http://127.0.0.1:8000/microsoft/login"

    const google = async () => {
        try {
            const res = await fetch(GOOGLE_SSO);
            const data = await res.json();
            router.push(data)
        } catch (err) {
            throw err;
        }
    }

    const microsoft = async () => {
        try {
            const res = await fetch(MICROSOFT_SSO);
            const data = await res.json();
            console.log(data)
            router.push(data.auth_uri)
        } catch (err) {
            throw err;
        }
    }

    return (
        <div>
            <button onClick={() => { google() }}>Google SSO</button>
            <button onClick={() => { microsoft() }}>Microsoft SSO</button>
        </div>
    )
}