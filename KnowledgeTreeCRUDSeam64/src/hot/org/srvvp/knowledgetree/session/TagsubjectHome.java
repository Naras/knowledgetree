package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import java.util.ArrayList;
import java.util.List;
import org.jboss.seam.annotations.In;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("tagsubjectHome")
public class TagsubjectHome extends EntityHome<Tagsubject> {

	@In(create = true)
	TagsubjectHome tagsubjectHome;

	public void setTagsubjectId(String id) {
		setId(id);
	}

	public String getTagsubjectId() {
		return (String) getId();
	}

	@Override
	protected Tagsubject createInstance() {
		Tagsubject tagsubject = new Tagsubject();
		return tagsubject;
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

	public Tagsubject getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

	public List<SubjectHasTag> getSubjectHasTags() {
		return getInstance() == null ? null : new ArrayList<SubjectHasTag>(
				getInstance().getSubjectHasTags());
	}
	public List<Tagsubject> getTagsubjects() {
		return getInstance() == null ? null : new ArrayList<Tagsubject>(
				getInstance().getTagsubjects());
	}

}
