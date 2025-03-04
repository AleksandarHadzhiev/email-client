import RoutersHandler from "./routersHandler";

export default class ExternalServiceHandler {

    static #instance: ExternalServiceHandler;
    private csrf: string = "";

    private constructor() { }

    public static get instance(): ExternalServiceHandler {
        if (!ExternalServiceHandler.#instance) {
            ExternalServiceHandler.#instance = new ExternalServiceHandler();
        }

        return ExternalServiceHandler.#instance;
    }

    async getToken(url: URL) {
        const routerHandler = new RoutersHandler(url, null)
        const body = await routerHandler.getHTTPMethod()
        this.setCSRF(body)
    }

    private setCSRF(body: any) {
        if ("csrf" in body) {
            this.csrf = body.csrf
        }
        else {
            alert("Unsupported error! Please try again later.")
        }
    }

    async login(data: any, url: URL) {
        const routerHandler = new RoutersHandler(url, this.csrf)
        const body = await routerHandler.postHTTPMethod(data = data)
        if ("redirect_uri" in body) {
            this.setCSRF(body)
            localStorage.setItem("token", this.csrf)
            return body.redirect_uri
        }
        else if ("error" in body) {
            alert(body.error.reason)
            return null
        }
        else {
            alert("Something went wrong. Please Try logging in again.")
            return null
        }
    }

    async auth(data: any, url: URL) {
        const csrf = localStorage.getItem('token') || ""
        localStorage.removeItem('token')
        const routerHandler = new RoutersHandler(url, csrf)
        const body = await routerHandler.postHTTPMethod(data = data)
        if ("token" in body && "email" in body) {
            this.setCSRF(body)
            return body
        }
        else if ("error" in body) {
            alert(body.error.reason)
            return null
        }
        else {
            alert("Something went wrong. Please Try logging in again.")
            return null
        }
    }

    async getMails(url: URL) {
        const routerHandler = new RoutersHandler(url, this.csrf)
        const body = await routerHandler.getHTTPMethod()
        if ("mails" in body && "csrf" in body) {
            this.setCSRF(body)
            return body.mails;
        }
        else if ("error" in body) {
            alert(body.error.reason)
            return null
        }
        else {
            alert("Something went wrong. Please Try logging in again.")
            return null
        }
    }

    async sendMessage(data: any, url: URL) {
        const routerHandler = new RoutersHandler(url, this.csrf)
        const body = await routerHandler.postHTTPMethod(data = data)
        if ("status" in body) {
            this.setCSRF(body)
            return body.status
        }
        else if ("error" in body) {
            alert(body.error.reason)
            return null
        }
        else {
            alert("Something went wrong. Please Try logging in again.")
            return null
        }
    }
}