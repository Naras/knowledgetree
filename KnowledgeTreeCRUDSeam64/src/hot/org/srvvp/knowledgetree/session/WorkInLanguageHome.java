package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.In;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("workInLanguageHome")
public class WorkInLanguageHome extends EntityHome<WorkInLanguage> {

	@In(create = true)
	LanguageHome languageHome;
	@In(create = true)
	WorkHome workHome;

	public void setWorkInLanguageId(WorkInLanguageId id) {
		setId(id);
	}

	public WorkInLanguageId getWorkInLanguageId() {
		return (WorkInLanguageId) getId();
	}

	public WorkInLanguageHome() {
		setWorkInLanguageId(new WorkInLanguageId());
	}

	@Override
	public boolean isIdDefined() {
		if (getWorkInLanguageId().getLanguage() == null
				|| "".equals(getWorkInLanguageId().getLanguage()))
			return false;
		if (getWorkInLanguageId().getWork() == null
				|| "".equals(getWorkInLanguageId().getWork()))
			return false;
		return true;
	}

	@Override
	protected WorkInLanguage createInstance() {
		WorkInLanguage workInLanguage = new WorkInLanguage();
		workInLanguage.setId(new WorkInLanguageId());
		return workInLanguage;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
		Language language = languageHome.getDefinedInstance();
		if (language != null) {
			getInstance().setLanguage(language);
		}
		Work work = workHome.getDefinedInstance();
		if (work != null) {
			getInstance().setWork(work);
		}
	}

	public boolean isWired() {
		if (getInstance().getLanguage() == null)
			return false;
		if (getInstance().getWork() == null)
			return false;
		return true;
	}

	public WorkInLanguage getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

}
