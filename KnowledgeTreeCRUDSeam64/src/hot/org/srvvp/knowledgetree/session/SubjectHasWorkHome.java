package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.In;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("subjectHasWorkHome")
public class SubjectHasWorkHome extends EntityHome<SubjectHasWork> {

	@In(create = true)
	SubjectHome subjectHome;
	@In(create = true)
	WorkHome workHome;
	@In(create = true)
	WorkSubjectRelationHome workSubjectRelationHome;

	public void setSubjectHasWorkId(SubjectHasWorkId id) {
		setId(id);
	}

	public SubjectHasWorkId getSubjectHasWorkId() {
		return (SubjectHasWorkId) getId();
	}

	public SubjectHasWorkHome() {
		setSubjectHasWorkId(new SubjectHasWorkId());
	}

	@Override
	public boolean isIdDefined() {
		if (getSubjectHasWorkId().getSubject() == null
				|| "".equals(getSubjectHasWorkId().getSubject()))
			return false;
		if (getSubjectHasWorkId().getWork() == null
				|| "".equals(getSubjectHasWorkId().getWork()))
			return false;
		if (getSubjectHasWorkId().getWorkSubjectRelation() == null
				|| "".equals(getSubjectHasWorkId().getWorkSubjectRelation()))
			return false;
		return true;
	}

	@Override
	protected SubjectHasWork createInstance() {
		SubjectHasWork subjectHasWork = new SubjectHasWork();
		subjectHasWork.setId(new SubjectHasWorkId());
		return subjectHasWork;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
		Subject subject = subjectHome.getDefinedInstance();
		if (subject != null) {
			getInstance().setSubject(subject);
		}
		Work work = workHome.getDefinedInstance();
		if (work != null) {
			getInstance().setWork(work);
		}
		WorkSubjectRelation workSubjectRelation = workSubjectRelationHome
				.getDefinedInstance();
		if (workSubjectRelation != null) {
			getInstance().setWorkSubjectRelation(workSubjectRelation);
		}
	}

	public boolean isWired() {
		if (getInstance().getSubject() == null)
			return false;
		if (getInstance().getWork() == null)
			return false;
		if (getInstance().getWorkSubjectRelation() == null)
			return false;
		return true;
	}

	public SubjectHasWork getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

}
