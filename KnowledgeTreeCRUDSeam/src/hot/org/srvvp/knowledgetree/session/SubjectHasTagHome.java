package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.In;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("subjectHasTagHome")
public class SubjectHasTagHome extends EntityHome<SubjectHasTag> {

	@In(create = true)
	SubjectHome subjectHome;
	@In(create = true)
	TagsubjectHome tagsubjectHome;

	public void setSubjectHasTagId(SubjectHasTagId id) {
		setId(id);
	}

	public SubjectHasTagId getSubjectHasTagId() {
		return (SubjectHasTagId) getId();
	}

	public SubjectHasTagHome() {
		setSubjectHasTagId(new SubjectHasTagId());
	}

	@Override
	public boolean isIdDefined() {
		if (getSubjectHasTagId().getSubject() == null
				|| "".equals(getSubjectHasTagId().getSubject()))
			return false;
		if (getSubjectHasTagId().getTag() == null
				|| "".equals(getSubjectHasTagId().getTag()))
			return false;
		return true;
	}

	@Override
	protected SubjectHasTag createInstance() {
		SubjectHasTag subjectHasTag = new SubjectHasTag();
		subjectHasTag.setId(new SubjectHasTagId());
		return subjectHasTag;
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
		Tagsubject tagsubject = tagsubjectHome.getDefinedInstance();
		if (tagsubject != null) {
			getInstance().setTagsubject(tagsubject);
		}
	}

	public boolean isWired() {
		if (getInstance().getSubject() == null)
			return false;
		if (getInstance().getTagsubject() == null)
			return false;
		return true;
	}

	public SubjectHasTag getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

}
