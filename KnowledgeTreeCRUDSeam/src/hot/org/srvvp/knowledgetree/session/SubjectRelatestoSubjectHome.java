package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.In;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("subjectRelatestoSubjectHome")
public class SubjectRelatestoSubjectHome
		extends
			EntityHome<SubjectRelatestoSubject> {

	@In(create = true)
	SubjectHome subjectHome;
	@In(create = true)
	SubjectSubjectRelationHome subjectSubjectRelationHome;

	public void setSubjectRelatestoSubjectId(SubjectRelatestoSubjectId id) {
		setId(id);
	}

	public SubjectRelatestoSubjectId getSubjectRelatestoSubjectId() {
		return (SubjectRelatestoSubjectId) getId();
	}

	public SubjectRelatestoSubjectHome() {
		setSubjectRelatestoSubjectId(new SubjectRelatestoSubjectId());
	}

	@Override
	public boolean isIdDefined() {
		if (getSubjectRelatestoSubjectId().getSubject1() == null
				|| "".equals(getSubjectRelatestoSubjectId().getSubject1()))
			return false;
		if (getSubjectRelatestoSubjectId().getSubject2() == null
				|| "".equals(getSubjectRelatestoSubjectId().getSubject2()))
			return false;
		return true;
	}

	@Override
	protected SubjectRelatestoSubject createInstance() {
		SubjectRelatestoSubject subjectRelatestoSubject = new SubjectRelatestoSubject();
		subjectRelatestoSubject.setId(new SubjectRelatestoSubjectId());
		return subjectRelatestoSubject;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
		Subject subjectBySubject1 = subjectHome.getDefinedInstance();
		if (subjectBySubject1 != null) {
			getInstance().setSubjectBySubject1(subjectBySubject1);
		}
		Subject subjectBySubject2 = subjectHome.getDefinedInstance();
		if (subjectBySubject2 != null) {
			getInstance().setSubjectBySubject2(subjectBySubject2);
		}
		SubjectSubjectRelation subjectSubjectRelation = subjectSubjectRelationHome
				.getDefinedInstance();
		if (subjectSubjectRelation != null) {
			getInstance().setSubjectSubjectRelation(subjectSubjectRelation);
		}
	}

	public boolean isWired() {
		if (getInstance().getSubjectBySubject1() == null)
			return false;
		if (getInstance().getSubjectBySubject2() == null)
			return false;
		return true;
	}

	public SubjectRelatestoSubject getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

}
