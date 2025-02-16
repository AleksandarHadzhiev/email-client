export default class RoutersHandler {

    constructor(private url: URL) {
    }

    async getHTTPMethod() {
        await fetch(this.url).then(async (res) => {
            const status = res.status
            if (status == 200) {
                return await res.json()
            }
            else if (status == 204) {
                return []
            }
            else {
                return res.json()
            }
        })
    }

    async postHTTPMethod(data: any) {
        const res = await fetch(this.url, { method: "POST", body: JSON.stringify(data) });
        return res;
    }

    async delteHTTPMethod() {
        await fetch(this.url, { method: "DELETE" }).then(async (res) => {
            const data = res
            return data
        }).catch((err) => {
            console.log(err)
        })
    }

    async putHTTPMethod(data: any) {
        const res = await fetch(this.url, { method: "PUT", body: JSON.stringify(data) });
        return res;
    }
}