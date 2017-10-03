package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import java.util.ArrayList;
import java.util.List;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("subjectHome")
public class SubjectHome extends EntityHome<Subject> {

	public void setSubjectId(String id) {
		setId(id);
	}

	public String getSubjectId() {
		return (String) getId();
	}

	@Override
	protected Subject createInstance() {
		Subject subject = new Subject();
		return subject;
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

	public Subject getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

	public List<SubjectHasTag> getSubjectHasTags() {
		return getInstance() == null ? null : new ArrayList<SubjectHasTag>(
				getInstance().getSubjectHasTags());
	}
	public List<SubjectHasWork> getSubjectHasWorks() {
		return getInstance() == null ? null : new ArrayList<SubjectHasWork>(
				getInstance().getSubjectHasWorks());
	}
	public List<SubjectRelatestoSubject> getSubjectRelatestoSubjectsForSubject1() {
		return getInstance() == null
				? null
				: new ArrayList<SubjectRelatestoSubject>(getInstance()
						.getSubjectRelatestoSubjectsForSubject1());
	}
	public List<SubjectRelatestoSubject> getSubjectRelatestoSubjectsForSubject2() {
		return getInstance() == null
				? null
				: new ArrayList<SubjectRelatestoSubject>(getInstance()
						.getSubjectRelatestoSubjectsForSubject2());
	}

}
