package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import java.util.ArrayList;
import java.util.List;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("workHome")
public class WorkHome extends EntityHome<Work> {

	public void setWorkId(String id) {
		setId(id);
	}

	public String getWorkId() {
		return (String) getId();
	}

	@Override
	protected Work createInstance() {
		Work work = new Work();
		return work;
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

	public Work getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

	public List<PersonHasWork> getPersonHasWorks() {
		return getInstance() == null ? null : new ArrayList<PersonHasWork>(
				getInstance().getPersonHasWorks());
	}
	public List<SubjectHasWork> getSubjectHasWorks() {
		return getInstance() == null ? null : new ArrayList<SubjectHasWork>(
				getInstance().getSubjectHasWorks());
	}
	public List<WorkHasTag> getWorkHasTags() {
		return getInstance() == null ? null : new ArrayList<WorkHasTag>(
				getInstance().getWorkHasTags());
	}
	public List<WorkInLanguage> getWorkInLanguages() {
		return getInstance() == null ? null : new ArrayList<WorkInLanguage>(
				getInstance().getWorkInLanguages());
	}
	public List<WorkInScript> getWorkInScripts() {
		return getInstance() == null ? null : new ArrayList<WorkInScript>(
				getInstance().getWorkInScripts());
	}
	public List<WorkRelatestoWork> getWorkRelatestoWorksForWork1() {
		return getInstance() == null ? null : new ArrayList<WorkRelatestoWork>(
				getInstance().getWorkRelatestoWorksForWork1());
	}
	public List<WorkRelatestoWork> getWorkRelatestoWorksForWork2() {
		return getInstance() == null ? null : new ArrayList<WorkRelatestoWork>(
				getInstance().getWorkRelatestoWorksForWork2());
	}

}
