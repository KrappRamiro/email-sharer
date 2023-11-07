import { getUserEmails } from "../utils/getUserEmails.mjs";
import { getCurrentUserId } from "../utils/getCurrentUserId.mjs";
import { EmailList } from "../components/emaillist.mjs";
import { Email } from "../components/email.mjs";
export class Paginator {
	constructor(goLeftBtn, goRightBtn, numOfElements, dots) {
		this.goLeftBtn = goLeftBtn;
		this.goRightBtn = goRightBtn;
		this.currentPagination = 0;
		this.currentUserId = getCurrentUserId();
		this.dots = dots;
		this.maxTabs = Math.ceil(numOfElements / 3);
		goLeftBtn.addEventListener("click", async () => {
			if (this.currentPagination == 0) {
				return;
			}
			this.currentPagination--;
			await this.renderEmails(this.currentPagination);
			this.colorizeBalls(this.currentPagination);
		});
		goRightBtn.addEventListener("click", async () => {
			if (this.currentPagination == this.maxTabs - 1) {
				return;
			}
			this.currentPagination++;
			await this.renderEmails(this.currentPagination);
			this.colorizeBalls(this.currentPagination);
		});
		this.colorizeBalls(this.currentPagination);
	}
	async renderEmails(pagination) {
		let emailList = new EmailList("#email-list");
		emailList.clear();
		const userEmails = await getUserEmails(this.currentUserId, pagination * 3);
		userEmails.forEach((emailData) => {
			const email = new Email(emailData);
			emailList.add(email.getHtmlElement());
		});
	}
	colorizeBalls(pagination) {
		if (pagination == 0) {
			this.dots[0].classList.add("active");
			this.dots[1].classList.remove("active");
			this.dots[2].classList.remove("active");
		} else if (pagination == this.maxTabs - 1) {
			this.dots[0].classList.remove("active");
			this.dots[1].classList.remove("active");
			this.dots[2].classList.add("active");
		} else {
			this.dots[0].classList.remove("active");
			this.dots[1].classList.add("active");
			this.dots[2].classList.remove("active");
		}
	}
}
