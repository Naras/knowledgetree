package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("viewSubjectWorkHome")
public class ViewSubjectWorkHome extends EntityHome<ViewSubjectWork> {

	public void setViewSubjectWorkId(ViewSubjectWorkId id) {
		setId(id);
	}

	public ViewSubjectWorkId getViewSubjectWorkId() {
		return (ViewSubjectWorkId) getId();
	}

	public ViewSubjectWorkHome() {
		setViewSubjectWorkId(new ViewSubjectWorkId());
	}

	@Override
	public boolean isIdDefined() {
		if (getViewSubjectWorkId().getRelation() == null
				|| "".equals(getViewSubjectWorkId().getRelation()))
			return false;
		if (getViewSubjectWorkId().getSubject() == null
				|| "".equals(getViewSubjectWorkId().getSubject()))
			return false;
		if (getViewSubjectWorkId().getWork() == null
				|| "".equals(getViewSubjectWorkId().getWork()))
			return false;
		return true;
	}

	@Override
	protected ViewSubjectWork createInstance() {
		ViewSubjectWork viewSubjectWork = new ViewSubjectWork();
		viewSubjectWork.setId(new ViewSubjectWorkId());
		return viewSubjectWork;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
	}

	public boolean isWired() {
		return true;
	}

	public ViewSubjectWork getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

}
