import { useState } from "react"

//@ts-ignore
export default function FullToDoContent({ todo, setIsOpened, setTrigeredEvent }) {

    const [title, setTitle] = useState(todo.title)
    const [desc, setDesc] = useState(todo.desc)
    const [date, setDate] = useState(todo.due)
    const CREATE_TODO_URL = "http://127.0.0.1:8000/todo/"

    const editToDo = (id: Number) => {
        const todo = {
            "title": title,
            "description": desc,
            "due_date": date,
            "email": "aleks321@gmail.com" // It will be an actual email
        }
        post(todo, id.toString())
    }

    const post = async (todo: { title: string; description: string; due_date: string; email: string }, id: String) => {
        await fetch(CREATE_TODO_URL + id, { method: "PUT", body: JSON.stringify(todo) }).then(async (res) => {
            const data = await res.json()
            setTrigeredEvent("edit")
        }).catch((err) => {
            alert(err)
        })
    }

    // 323232 / 292929 / 272727 / 222222
    // const openedBodyToDoStructure = "flex flex-row h-full w-full bg-[#1C1C1C]"

    return (
        <div className="w-1/3 h-full bg-[#323232] flex flex-col space-y-12">
            <button
                onClick={() => { setIsOpened(false) }}
                className="absolute right-0 px-2 py-1 bg-transparent border-2 border-gray-200 hover:border-gray-400 hover:text-gray-400">X</button>
            <div id="title" className="ml-2 w-[96%] bg-[#292929] h-24">
                <textarea className="px-2 py-1 w-full h-full bg-transparent text-white" value={title} onChange={(e) => { setTitle(e.target.value) }} onMouseLeave={() => { editToDo(todo.id) }} />
            </div>
            <div id="date" className="ml-2 w-[96%] h-12 bg-[#292929] flex">
                <input
                    id="dueDate"
                    className="bg-transparent text-gray-200 border-2 rounded-md"
                    datepicker-format="mm-dd-yyyy"
                    type="date"
                    value={date}
                    onChange={e => { setDate(e.currentTarget.value); }}
                    onMouseLeave={() => { editToDo(todo.id) }}
                />
                <p className="self-center w-[80%]">Due date</p>
            </div>
            <div id="desc" className="ml-2 w-[96%] bg-[#292929] h-24">
                <textarea className="px-2 py-1 w-full h-full bg-transparent text-white" value={desc} onChange={(e) => { setDesc(e.target.value) }} onMouseLeave={() => { editToDo(todo.id) }} />
            </div>
        </div>
    )
}