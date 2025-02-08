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
        console.log(todo)
        post(todo, id.toString())
    }

    const post = async (todo: { title: string; description: string; due_date: string; email: string }, id: String) => {
        await fetch(CREATE_TODO_URL + id, { method: "PUT", body: JSON.stringify(todo) }).then(async (res) => {
            const data = await res.json()
            console.log(data)
            setTrigeredEvent("edit")
        }).catch((err) => {
            console.log(err)
        })
    }

    return (
        <div className="w-1/3 h-full bg-gray-700 flex flex-col space-y-12">
            <button
                onClick={() => { setIsOpened(false) }}
                className="absolute right-0 px-2 py-1 bg-transparent border-2 border-gray-200 hover:border-gray-400 hover:text-gray-400">X</button>
            <div id="title" className="w-[96%] ml-2 mr-2 bg-gray-900 w-full h-24">
                <textarea className="w-full h-full bg-transparent text-white" value={title} onChange={(e) => { setTitle(e.target.value) }} onMouseLeave={() => { editToDo(todo.id) }} />
            </div>
            <div id="date" className="w-[96%] ml-2 mr-2 bg-gray-900 h-12 flex">
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
            <div id="desc" className="w-[96%] ml-2 mr-2 bg-gray-900 h-24">
                <textarea className="w-full h-full bg-transparent text-white" value={desc} onChange={(e) => { setDesc(e.target.value) }} onMouseLeave={() => { editToDo(todo.id) }} />
            </div>
        </div>
    )
}