package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("viewSubjectSubjectHome")
public class ViewSubjectSubjectHome extends EntityHome<ViewSubjectSubject> {

	public void setViewSubjectSubjectId(ViewSubjectSubjectId id) {
		setId(id);
	}

	public ViewSubjectSubjectId getViewSubjectSubjectId() {
		return (ViewSubjectSubjectId) getId();
	}

	public ViewSubjectSubjectHome() {
		setViewSubjectSubjectId(new ViewSubjectSubjectId());
	}

	@Override
	public boolean isIdDefined() {
		if (getViewSubjectSubjectId().getRelation() == null
				|| "".equals(getViewSubjectSubjectId().getRelation()))
			return false;
		if (getViewSubjectSubjectId().getRelationDescription() == null
				|| ""
						.equals(getViewSubjectSubjectId()
								.getRelationDescription()))
			return false;
		if (getViewSubjectSubjectId().getSub1id() == null
				|| "".equals(getViewSubjectSubjectId().getSub1id()))
			return false;
		if (getViewSubjectSubjectId().getSub2id() == null
				|| "".equals(getViewSubjectSubjectId().getSub2id()))
			return false;
		if (getViewSubjectSubjectId().getSubject1() == null
				|| "".equals(getViewSubjectSubjectId().getSubject1()))
			return false;
		if (getViewSubjectSubjectId().getSubject1description() == null
				|| ""
						.equals(getViewSubjectSubjectId()
								.getSubject1description()))
			return false;
		if (getViewSubjectSubjectId().getSubject2() == null
				|| "".equals(getViewSubjectSubjectId().getSubject2()))
			return false;
		if (getViewSubjectSubjectId().getSubject2description() == null
				|| ""
						.equals(getViewSubjectSubjectId()
								.getSubject2description()))
			return false;
		return true;
	}

	@Override
	protected ViewSubjectSubject createInstance() {
		ViewSubjectSubject viewSubjectSubject = new ViewSubjectSubject();
		viewSubjectSubject.setId(new ViewSubjectSubjectId());
		return viewSubjectSubject;
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

	public ViewSubjectSubject getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

}
